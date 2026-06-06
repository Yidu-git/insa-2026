"""CTF Lab - Vulnerable Web Application VulnCorp Internal Portal v2.4.1"""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
from functools import wraps

from flask import (
    Flask,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    render_template_string,
    request,
    send_from_directory,
    session,
    url_for,
)
from jinja2 import Environment, FileSystemLoader, SandboxedEnvironment
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey_vulncorp_2024"  # Intentionally weak

# ── Config ─────────────────────────────────────────────────────────────────
UPLOAD_FOLDER = "/app/uploads"
ALLOWED_EXTENSIONS_WEAK = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "pdf",
    "txt",
    "php",
    "phtml",
}
DATABASE = "/app/db/vulncorp.db"

FLAG_RECON = "FLAG{r3c0n_m4st3r_r0b0ts_txt}"
FLAG_SQLI = "FLAG{sql1_4uth_byp4ss_pwn3d}"
FLAG_IDOR = "FLAG{1d0r_ch4mp_acc3ss_d3n13d_lol}"
FLAG_BAC = "FLAG{brok3n_4cc3ss_c0ntr0l_0wn3d}"
FLAG_XSS = "FLAG{x55_st0r3d_c00k13_st0l3n}"
FLAG_SSTI = "FLAG{5st1_t3mpl4t3_1nj3ct10n_rce}"
FLAG_UPLOAD = "FLAG{f1l3_upl04d_w3bsh3ll_dr0pp3d}"
FLAG_RCE = "FLAG{rce_full_pwn_y0u_0wn_th3_b0x}"
FLAG_HIDDEN = "FLAG{p4ss1v3_r3c0n_m3t4d4t4_l34k}"
FLAG_BONUS = "FLAG{s3c0nd_0rd3r_sql1_d4ng3r0us}"

SSTI_FLAG_DIR = os.path.join(os.path.dirname(__file__), "flags")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SSTI_FLAG_DIR, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ── Database ────────────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript(
        f"""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        email TEXT,
        notes TEXT DEFAULT '',
        approved INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        title TEXT,
        content TEXT,
        is_private INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        message TEXT,
        reviewed INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY,
        bio TEXT,
        department TEXT,
        template_field TEXT
    );
    INSERT OR IGNORE INTO users (username, password, role, email, notes, approved) VALUES 
    ('admin', '5f4dcc3b5aa765d61d8327deb882cf99', 'admin', 'admin@vulncorp.internal', 'Admin account - do not share', 1),
    ('alice', 'ef92b778bafe771e89245b89ecbc08a6', 'user', 'alice@vulncorp.com', '{FLAG_IDOR}', 1),
    ('bob', '1a79a4d60de6718e8e5b326e338ae533', 'user', 'bob@vulncorp.com', 'Nothing special here', 1),
    ('charlie', 'a87ff679a2f3e71d9181a67b7542122c', 'user', 'charlie@vulncorp.com', 'I love CTFs', 1);
    
    INSERT OR IGNORE INTO documents (owner_id, title, content, is_private) VALUES 
    (1, 'Admin Secret', 'Top secret data. {FLAG_BAC}', 1),
    (2, 'Alice Notes', 'My personal notes.', 1),
    (3, 'Bobs Public', 'Nothing to see.', 0),
    (1, 'Server Creds', 'ssh root@10.10.10.1 pass=r00t_v4ult', 1);
    
    INSERT OR IGNORE INTO profiles (id, bio, department, template_field) VALUES 
    (1, 'Site administrator.', 'IT', 'Welcome Admin'),
    (2, 'Developer.', 'Engineering', 'Welcome Alice');
    """
    )
    db.commit()

    # Migration: add approved column if upgrading from older schema
    user_cols = [r[1] for r in db.execute("PRAGMA table_info(users)").fetchall()]
    if "approved" not in user_cols:
        db.execute("ALTER TABLE users ADD COLUMN approved INTEGER DEFAULT 0")
        db.execute(
            "UPDATE users SET approved=1 WHERE username IN ('admin','alice','bob','charlie')"
        )
        db.commit()

    cols = [r[1] for r in db.execute("PRAGMA table_info(documents)").fetchall()]
    if "doc_key" not in cols:
        db.execute("ALTER TABLE documents ADD COLUMN doc_key TEXT")
        db.commit()

    if "doc_key" in [
        r[1] for r in db.execute("PRAGMA table_info(documents)").fetchall()
    ]:
        db.execute(
            "UPDATE documents SET doc_key = 'DOC-' || printf('%03d', id) WHERE doc_key IS NULL"
        )
        db.commit()
    db.close()


# ── Auth Helpers ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            return (
                render_template(
                    "error.html", msg="Access Denied — Admins only.", code=403
                ),
                403,
            )
        return f(*args, **kwargs)

    return decorated


def approved_required(f):
    """Blocks unapproved (self-registered) users from sensitive features.

    Admin role is always exempt — approval only applies to regular users.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("approved") and session.get("role") != "admin":
            return (
                render_template(
                    "restricted.html",
                    feature=getattr(f, "__name__", "this feature"),
                ),
                403,
            )
        return f(*args, **kwargs)

    return decorated


# ── Middleware: hidden flag in response header ───────────────────────────────
@app.after_request
def add_hidden_header(response):
    response.headers["X-Debug-Token"] = FLAG_HIDDEN
    response.headers["X-Powered-By"] = "VulnCorp-Portal/2.4.1 Flask/2.3"
    response.headers["Server"] = "Apache/2.4.51 (Debian)"  # fake
    return response


# ── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# robots.txt — recon flag
@app.route("/robots.txt")
def robots():
    content = f"""User-agent: *
Disallow: /admin
Disallow: /api
Disallow: /backup
Disallow: /internal
# FLAG: {FLAG_RECON}
# Note: removed old /secret-panel route, but /admin-old still exists
"""
    return app.response_class(content, mimetype="text/plain")


# ── Auth ─────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        password_hash = hashlib.md5(password.encode()).hexdigest()

        # VULN: SQLi — no parameterised query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
        try:
            db = get_db()
            user = db.execute(query).fetchone()
            if user:
                if user["role"] == "admin":
                    error = "Admin users must authenticate through the dedicated admin panel."
                else:
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["role"] = user["role"]
                    session["approved"] = bool(user["approved"])
                    if any(tok in username for tok in ["'", "--", ";"]):
                        session["sqli_flag"] = FLAG_SQLI
                    return redirect(url_for("dashboard"))
            else:
                error = "Invalid credentials."
        except Exception as e:
            error = f"DB Error: {e}"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")
        db = get_db()

        # VULN: Second-order SQLi — stores raw username, used unsafely later in /profile/update
        try:
            pw_hash = hashlib.md5(password.encode()).hexdigest()
            db.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, pw_hash, email),
            )
            db.commit()

            # Create profile
            uid = db.execute(
                "SELECT id FROM users WHERE username=?", (username,)
            ).fetchone()["id"]
            db.execute(
                "INSERT INTO profiles (id, bio, department, template_field) VALUES (?, '', 'General', 'Welcome')",
                (uid,),
            )
            db.commit()
            return redirect(url_for("login"))
        except Exception as e:
            error = f"Registration error: {e}"
    return render_template("register.html", error=error)


# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    docs = db.execute(
        "SELECT * FROM documents WHERE owner_id=? OR is_private=0",
        (session["user_id"],),
    ).fetchall()
    return render_template("dashboard.html", documents=docs)
