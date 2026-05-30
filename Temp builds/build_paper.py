from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.colors import HexColor
import datetime

# ── Color Palette ──────────────────────────────────────────────────────────────
DARK_BG     = HexColor("#0D1117")
ACCENT      = HexColor("#00FF88")
ACCENT2     = HexColor("#00BFFF")
TEXT_MAIN   = HexColor("#E6EDF3")
TEXT_MUTED  = HexColor("#8B949E")
TABLE_HDR   = HexColor("#161B22")
TABLE_ALT   = HexColor("#0D1117")
TABLE_ROW   = HexColor("#161B22")
CODE_BG     = HexColor("#161B22")
RED_WARN    = HexColor("#FF4444")
GOLD        = HexColor("#FFD700")
PURPLE      = HexColor("#9D4EDD")

OUTPUT = "/mnt/user-data/outputs/Reverse_Engineering_Cybersecurity_Pro_Guide.pdf"

# ── Custom Page Template ───────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    # Dark background
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Top accent bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h - 6, w, 6, fill=1, stroke=0)
    # Bottom bar
    canvas.setFillColor(TABLE_HDR)
    canvas.rect(0, 0, w, 28, fill=1, stroke=0)
    # Page number
    canvas.setFillColor(TEXT_MUTED)
    canvas.setFont("Courier", 8)
    canvas.drawCentredString(w / 2, 10, f"Page {doc.page}  |  Reverse Engineering: Pro Cybersecurity Guide  |  Confidential")
    # Side accent line
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(2)
    canvas.line(30, 40, 30, h - 20)
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.restoreState()

# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    s = {}

    s['cover_title'] = ParagraphStyle('cover_title',
        fontSize=38, textColor=ACCENT, alignment=TA_CENTER,
        fontName='Helvetica-Bold', leading=46, spaceAfter=8)

    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontSize=16, textColor=ACCENT2, alignment=TA_CENTER,
        fontName='Helvetica', leading=22, spaceAfter=6)

    s['cover_meta'] = ParagraphStyle('cover_meta',
        fontSize=11, textColor=TEXT_MUTED, alignment=TA_CENTER,
        fontName='Courier', leading=16)

    s['chapter'] = ParagraphStyle('chapter',
        fontSize=22, textColor=ACCENT, fontName='Helvetica-Bold',
        leading=28, spaceBefore=14, spaceAfter=10,
        borderPad=4)

    s['section'] = ParagraphStyle('section',
        fontSize=14, textColor=ACCENT2, fontName='Helvetica-Bold',
        leading=20, spaceBefore=10, spaceAfter=5)

    s['subsection'] = ParagraphStyle('subsection',
        fontSize=11, textColor=GOLD, fontName='Helvetica-Bold',
        leading=16, spaceBefore=7, spaceAfter=3)

    s['body'] = ParagraphStyle('body',
        fontSize=9.5, textColor=TEXT_MAIN, fontName='Helvetica',
        leading=15, spaceAfter=5, alignment=TA_JUSTIFY,
        leftIndent=10)

    s['bullet'] = ParagraphStyle('bullet',
        fontSize=9.5, textColor=TEXT_MAIN, fontName='Helvetica',
        leading=15, spaceAfter=3, leftIndent=22, bulletIndent=10)

    s['code'] = ParagraphStyle('code',
        fontSize=8.5, textColor=ACCENT, fontName='Courier',
        leading=13, spaceAfter=2, leftIndent=24,
        backColor=CODE_BG)

    s['code_comment'] = ParagraphStyle('code_comment',
        fontSize=8.5, textColor=TEXT_MUTED, fontName='Courier',
        leading=13, spaceAfter=2, leftIndent=24,
        backColor=CODE_BG)

    s['warning'] = ParagraphStyle('warning',
        fontSize=9, textColor=RED_WARN, fontName='Helvetica-Bold',
        leading=13, spaceBefore=4, spaceAfter=4,
        leftIndent=10, borderColor=RED_WARN, borderWidth=1, borderPad=4)

    s['tip'] = ParagraphStyle('tip',
        fontSize=9, textColor=ACCENT, fontName='Helvetica-Oblique',
        leading=13, spaceBefore=4, spaceAfter=4,
        leftIndent=10)

    s['toc_title'] = ParagraphStyle('toc_title',
        fontSize=18, textColor=ACCENT, fontName='Helvetica-Bold',
        alignment=TA_CENTER, leading=24, spaceAfter=16)

    s['toc_entry'] = ParagraphStyle('toc_entry',
        fontSize=10, textColor=TEXT_MAIN, fontName='Helvetica',
        leading=18, leftIndent=20)

    s['toc_sub'] = ParagraphStyle('toc_sub',
        fontSize=9, textColor=TEXT_MUTED, fontName='Helvetica',
        leading=16, leftIndent=44)

    return s

# ── Table helper ───────────────────────────────────────────────────────────────
def make_table(data, col_widths, hdr_rows=1):
    t = Table(data, colWidths=col_widths, repeatRows=hdr_rows)
    style = [
        ('BACKGROUND', (0,0), (-1, hdr_rows-1), TABLE_HDR),
        ('TEXTCOLOR',  (0,0), (-1, hdr_rows-1), ACCENT),
        ('FONTNAME',   (0,0), (-1, hdr_rows-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1, hdr_rows-1), 9),
        ('ALIGN',      (0,0), (-1,-1),           'LEFT'),
        ('VALIGN',     (0,0), (-1,-1),           'TOP'),
        ('FONTNAME',   (0,hdr_rows), (-1,-1),    'Helvetica'),
        ('FONTSIZE',   (0,hdr_rows), (-1,-1),    8.5),
        ('TEXTCOLOR',  (0,hdr_rows), (-1,-1),    TEXT_MAIN),
        ('ROWBACKGROUNDS', (0, hdr_rows), (-1,-1), [TABLE_ALT, TABLE_ROW]),
        ('GRID',       (0,0), (-1,-1),           0.4, HexColor("#30363D")),
        ('TOPPADDING', (0,0), (-1,-1),           5),
        ('BOTTOMPADDING',(0,0),(-1,-1),          5),
        ('LEFTPADDING',(0,0), (-1,-1),           7),
        ('RIGHTPADDING',(0,0),(-1,-1),           7),
    ]
    t.setStyle(TableStyle(style))
    return t

def hr(s):
    return HRFlowable(width="100%", thickness=0.5, color=HexColor("#30363D"),
                      spaceAfter=6, spaceBefore=6)

# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    doc = BaseDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=0.65*inch, rightMargin=0.55*inch,
        topMargin=0.55*inch, bottomMargin=0.55*inch
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='normal')
    doc.addPageTemplates([
        PageTemplate(id='cover', frames=[frame], onPage=on_first_page),
        PageTemplate(id='body',  frames=[frame], onPage=on_page),
    ])

    s  = make_styles()
    st = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Spacer(1, 1.1*inch))
    st.append(Paragraph("REVERSE ENGINEERING", s['cover_title']))
    st.append(Paragraph("The Complete Professional Guide to Cybersecurity", s['cover_sub']))
    st.append(Spacer(1, 0.15*inch))
    # accent line
    st.append(HRFlowable(width="60%", thickness=2, color=ACCENT,
                         hAlign='CENTER', spaceAfter=14, spaceBefore=6))
    st.append(Paragraph("Tools · Techniques · Methodology · Step-by-Step Workflows", s['cover_meta']))
    st.append(Spacer(1, 0.35*inch))

    # cover info box
    cover_data = [
        [Paragraph("<b>CLASSIFICATION</b>", ParagraphStyle('x', textColor=ACCENT,   fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Educational / Research Use Only", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=9))],
        [Paragraph("<b>VERSION</b>",         ParagraphStyle('x', textColor=ACCENT,   fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("2.0 — 2025 Edition",     ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=9))],
        [Paragraph("<b>PAGES</b>",           ParagraphStyle('x', textColor=ACCENT,   fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("15+  |  In-Depth Coverage", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=9))],
        [Paragraph("<b>AUDIENCE</b>",        ParagraphStyle('x', textColor=ACCENT,   fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Aspiring & Professional Security Researchers", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=9))],
    ]
    ct = Table(cover_data, colWidths=[1.6*inch, 4.2*inch])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TABLE_HDR),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#30363D")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    st.append(ct)
    st.append(Spacer(1, 0.4*inch))
    st.append(HRFlowable(width="80%", thickness=1, color=ACCENT2,
                         hAlign='CENTER', spaceAfter=12))
    st.append(Paragraph(
        "⚠  This paper is intended solely for educational purposes, ethical security research,\n"
        "and authorized penetration testing. Unauthorized use against systems you do not own\n"
        "or have explicit written permission to test is illegal and unethical.",
        ParagraphStyle('disc', fontSize=8.5, textColor=RED_WARN,
                       fontName='Helvetica-Oblique', alignment=TA_CENTER, leading=14)))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("TABLE OF CONTENTS", s['toc_title']))
    st.append(hr(s))
    toc = [
        ("1.", "Introduction to Reverse Engineering", [
            "1.1 What Is Reverse Engineering?",
            "1.2 History & Evolution",
            "1.3 Why It Matters in Cybersecurity",
        ]),
        ("2.", "Legal & Ethical Framework", [
            "2.1 Laws & Regulations (CFAA, GDPR, DMCA)",
            "2.2 Responsible Disclosure",
            "2.3 Bug Bounty Programs",
        ]),
        ("3.", "Foundational Knowledge", [
            "3.1 Computer Architecture Essentials",
            "3.2 Assembly Language Primer",
            "3.3 File Formats & Binary Structure",
            "3.4 Operating System Internals",
        ]),
        ("4.", "The Reverse Engineering Toolkit", [
            "4.1 Disassemblers & Decompilers",
            "4.2 Debuggers",
            "4.3 Dynamic Analysis Tools",
            "4.4 Network Analysis Tools",
            "4.5 Hex Editors & Binary Analysis",
            "4.6 Specialized & Bonus Tools",
        ]),
        ("5.", "Static Analysis — Step-by-Step", [
            "5.1 Initial Reconnaissance",
            "5.2 Disassembly Workflow",
            "5.3 Decompilation & Code Recovery",
            "5.4 String & Import Analysis",
        ]),
        ("6.", "Dynamic Analysis — Step-by-Step", [
            "6.1 Setting Up a Safe Lab Environment",
            "6.2 Debugging a Binary",
            "6.3 API Monitoring & Hooking",
            "6.4 Memory Forensics",
        ]),
        ("7.", "Malware Analysis Deep Dive", [
            "7.1 Malware Classification",
            "7.2 Unpacking & Deobfuscation",
            "7.3 Behavioral Analysis",
            "7.4 C2 Infrastructure Mapping",
        ]),
        ("8.", "Vulnerability Research", [
            "8.1 Fuzzing Techniques",
            "8.2 Identifying Memory Corruption Bugs",
            "8.3 Writing a Proof-of-Concept Exploit",
        ]),
        ("9.", "Advanced Techniques", [
            "9.1 Anti-Reversing Bypass",
            "9.2 Firmware & Embedded Systems",
            "9.3 Android & iOS Reverse Engineering",
            "9.4 Symbolic Execution & Automated Analysis",
        ]),
        ("10.", "Building Your Pro Workflow & Career Path", [
            "10.1 CTF Challenges & Practice Labs",
            "10.2 Certifications & Learning Resources",
            "10.3 Professional Career Roadmap",
        ]),
    ]
    for num, title, subs in toc:
        st.append(Paragraph(f"<b>{num}</b>  {title}", s['toc_entry']))
        for sub in subs:
            st.append(Paragraph(f"• {sub}", s['toc_sub']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 1 — INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("1. Introduction to Reverse Engineering", s['chapter']))
    st.append(hr(s))

    st.append(Paragraph("1.1  What Is Reverse Engineering?", s['section']))
    st.append(Paragraph(
        "Reverse engineering (RE) is the process of analyzing a system — software, hardware, "
        "firmware, or protocol — to understand its design, function, and operation without "
        "access to the original source code or blueprints. In cybersecurity, it is the "
        "foundational skill that enables security researchers to dissect malware, discover "
        "vulnerabilities, audit closed-source software, and develop defensive capabilities. "
        "Unlike traditional software development, which moves from specification to product, "
        "reverse engineering works backwards: from the compiled binary back to human-readable "
        "logic.", s['body']))
    st.append(Paragraph(
        "At its core, RE combines computer science, detective work, and creative thinking. "
        "A skilled reverse engineer must simultaneously understand low-level machine code, "
        "high-level program logic, operating system internals, and attacker psychology. "
        "This multi-disciplinary nature makes it one of the most challenging and most "
        "rewarding specializations in the entire field of cybersecurity.", s['body']))

    st.append(Paragraph("1.2  History & Evolution", s['section']))
    st.append(Paragraph(
        "Reverse engineering predates digital computers — mechanical engineers have always "
        "disassembled competitors' products to understand their mechanisms. In computing, RE "
        "became significant in the 1980s when companies reverse engineered IBM's BIOS to "
        "create compatible PC clones, launching the personal computer revolution. "
        "The 1990s saw RE weaponized for both offense (early virus writers) and defense "
        "(the first antivirus researchers). The 2000s brought sophisticated nation-state "
        "malware: Stuxnet (2010) — a joint US/Israeli operation targeting Iranian nuclear "
        "centrifuges — was entirely uncovered through reverse engineering and remains the "
        "most studied piece of malware in history. Today, RE drives bug bounty programs, "
        "threat intelligence, and zero-day research at organizations like Google Project Zero, "
        "NSA, and every major cybersecurity vendor.", s['body']))

    st.append(Paragraph("1.3  Why It Matters in Cybersecurity", s['section']))
    reasons = [
        ("Malware Analysis", "Understanding how malicious code operates enables defenders to build detection rules, patch victims, and attribute attacks."),
        ("Vulnerability Research", "Finding bugs in closed-source software before attackers do, enabling patches and responsible disclosure."),
        ("Penetration Testing", "Reversing client applications, APIs, and firmware to identify attack surface during authorized engagements."),
        ("Threat Intelligence", "Extracting indicators of compromise (IoCs), C2 infrastructure details, and actor TTPs from malware samples."),
        ("Protocol Reverse Engineering", "Reconstructing undocumented network protocols used by malware or proprietary devices."),
        ("Software Interoperability", "Creating compatible implementations when documentation is unavailable — the legal basis for tools like Wine."),
    ]
    for title, desc in reasons:
        st.append(Paragraph(f"<b><font color='#00FF88'>▸ {title}:</font></b>  {desc}", s['bullet']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 2 — LEGAL & ETHICAL
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("2. Legal & Ethical Framework", s['chapter']))
    st.append(hr(s))
    st.append(Paragraph(
        "<b><font color='#FF4444'>⚠ CRITICAL:</font></b>  Before touching any tool or binary, "
        "understand that unauthorized reverse engineering of systems you do not own is a "
        "criminal offense in most jurisdictions. Always work within explicit legal authorization.",
        s['warning']))

    st.append(Paragraph("2.1  Key Laws & Regulations", s['section']))
    law_data = [
        [Paragraph("Law / Regulation", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Jurisdiction", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Relevance to Reverse Engineering", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Computer Fraud & Abuse Act (CFAA)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("USA", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Prohibits unauthorized access; RE on systems you don't own is illegal", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Digital Millennium Copyright Act (DMCA) §1201", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("USA", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Restricts circumventing DRM/copy protection; security research exemptions exist", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Computer Misuse Act 1990", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("UK", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Unauthorized access to computer material is a criminal offense", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("GDPR Article 32", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("EU", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("RE that exposes personal data requires careful handling and notification", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Software Directive 2009/24/EC Art.6", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("EU", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Permits RE for interoperability purposes only", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(law_data, [2.1*inch, 0.85*inch, 3.3*inch]))
    st.append(Spacer(1, 8))

    st.append(Paragraph("2.2  Responsible Disclosure", s['section']))
    st.append(Paragraph(
        "When you discover a vulnerability through RE, responsible disclosure is the ethical "
        "and often legally protective path. The standard process: (1) Document the finding "
        "thoroughly. (2) Contact the vendor's security team privately (find security.txt or "
        "the security contact). (3) Give them a reasonable remediation window — typically "
        "90 days, per Google Project Zero's standard. (4) If unresponsive, escalate to "
        "CERT/CC or publish a coordinated advisory. Never sell 0-days to brokers without "
        "understanding the legal and ethical consequences.", s['body']))

    st.append(Paragraph("2.3  Bug Bounty Programs", s['section']))
    st.append(Paragraph(
        "Bug bounty platforms like HackerOne, Bugcrowd, and Intigriti provide legal frameworks "
        "for security research. Companies explicitly invite researchers to find vulnerabilities "
        "in their systems within defined scopes. Payouts range from $100 for minor bugs to "
        "$1,000,000+ for critical zero-days on platforms like Apple Security Research. "
        "Always read and respect the program scope — testing out-of-scope targets voids "
        "legal protections.", s['body']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 3 — FOUNDATIONS
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("3. Foundational Knowledge", s['chapter']))
    st.append(hr(s))
    st.append(Paragraph(
        "Reverse engineering without foundational knowledge is like trying to read a novel "
        "in an unknown language. You must be fluent in the following disciplines before "
        "attempting serious RE work.", s['body']))

    st.append(Paragraph("3.1  Computer Architecture Essentials", s['section']))
    st.append(Paragraph(
        "You must deeply understand the <b><font color='#00BFFF'>x86/x86-64</font></b> "
        "instruction set architecture (ISA) as it powers most desktop malware and CTF "
        "challenges. Also gain familiarity with <b><font color='#00BFFF'>ARM</font></b> "
        "(mobile devices, embedded systems, Apple Silicon) and "
        "<b><font color='#00BFFF'>MIPS/RISC-V</font></b> (routers, IoT).", s['body']))

    arch_data = [
        [Paragraph("Concept", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Why It Matters for RE", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Registers (EAX, RIP, ESP...)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Every instruction operates on registers; understanding their purpose lets you trace data flow", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Stack & Calling Conventions", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Function arguments, local variables, and return addresses all live on the stack — critical for exploit dev", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Memory Segments (.text/.data/.bss)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Knowing where code, globals, and BSS live helps locate interesting data quickly", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Endianness (little vs big)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Affects how multi-byte values are stored; critical when reading hex dumps", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("System Calls (syscalls)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Interface between user-space code and the OS kernel; malware heavily uses syscalls to evade user-mode hooks", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(arch_data, [2.2*inch, 4.0*inch]))

    st.append(Paragraph("3.2  Assembly Language Primer", s['section']))
    st.append(Paragraph(
        "You do not need to write assembly from scratch, but you must be able to read and "
        "understand it fluently. Compiled programs are displayed as assembly in disassemblers. "
        "Key instructions to master:", s['body']))
    asm_lines = [
        ("mov eax, 0x1337",   "; Move value 0x1337 into register EAX"),
        ("push ebp",          "; Save base pointer (function prologue)"),
        ("call 0x401000",     "; Call function at address 0x401000"),
        ("cmp eax, 0",        "; Compare EAX to zero (sets flags)"),
        ("jz  0x40101A",      "; Jump if zero flag set (conditional branch)"),
        ("lea ecx, [ebx+4]",  "; Load effective address — pointer arithmetic"),
        ("xor eax, eax",      "; Fast way to zero EAX (common compiler idiom)"),
        ("ret",               "; Return from function (pops RIP from stack)"),
    ]
    for instr, comment in asm_lines:
        st.append(Paragraph(f"{instr:<30}{comment}", s['code']))

    st.append(Paragraph("3.3  File Formats & Binary Structure", s['section']))
    st.append(Paragraph(
        "Different platforms use different executable formats. A reverse engineer must "
        "recognize and parse each:", s['body']))
    fmt_data = [
        [Paragraph("Format", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Platform", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Magic Bytes", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Key Structures", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("PE (Portable Executable)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Windows (.exe/.dll)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("4D 5A (MZ)", ParagraphStyle('x', textColor=ACCENT, fontName='Courier', fontSize=8.5)),
         Paragraph("DOS header, PE header, section table, import/export tables", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("ELF (Executable & Linkable Format)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Linux/Android", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("7F 45 4C 46", ParagraphStyle('x', textColor=ACCENT, fontName='Courier', fontSize=8.5)),
         Paragraph("ELF header, program/section headers, symbol table, dynamic section", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Mach-O", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("macOS/iOS", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("CE FA ED FE", ParagraphStyle('x', textColor=ACCENT, fontName='Courier', fontSize=8.5)),
         Paragraph("Load commands, segments, fat binary headers (universal binary)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("DEX (Dalvik Executable)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Android", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("64 65 78 0A", ParagraphStyle('x', textColor=ACCENT, fontName='Courier', fontSize=8.5)),
         Paragraph("String/type/method pools, class definitions, bytecode", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(fmt_data, [1.7*inch, 1.15*inch, 0.95*inch, 2.45*inch]))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 4 — THE TOOLKIT
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("4. The Reverse Engineering Toolkit", s['chapter']))
    st.append(hr(s))
    st.append(Paragraph(
        "Choosing the right tool for each task is half the battle. Below is a comprehensive "
        "breakdown of every essential tool, what it does, and when to use it.", s['body']))

    st.append(Paragraph("4.1  Disassemblers & Decompilers", s['section']))
    dis_data = [
        [Paragraph("Tool", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Type", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Cost", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Primary Use", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Strengths", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("IDA Pro", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Disassembler + Decompiler", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$1,499+", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Industry-standard for malware analysis & vuln research", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Best architecture support, Hex-Rays decompiler, mature plugin ecosystem (IDAPython)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Ghidra", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Disassembler + Decompiler", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("FREE (NSA)", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Full-featured alternative to IDA; great for beginners", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Excellent decompiler, collaborative features, Java/Python scripting, runs on all OSes", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Binary Ninja", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Disassembler + Decompiler", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$299+", ParagraphStyle('x', textColor=TEXT_MUTED, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Automated analysis, API-first design, CI/CD integration", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Python API, intermediate language (BNIL), headless mode, modern UI", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Radare2 / Cutter", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Framework + GUI", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("FREE", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Command-line RE framework; Cutter is its Qt GUI frontend", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Scripting (r2pipe), embedded systems, forensics, highly portable", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("RetDec", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Decompiler", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("FREE", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Automated decompilation to C, cloud or local API", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Good for quick automated analysis, integrates with other tools", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(dis_data, [1.0*inch, 1.3*inch, 0.7*inch, 1.6*inch, 1.75*inch]))

    st.append(Paragraph("4.2  Debuggers", s['section']))
    dbg_data = [
        [Paragraph("Tool", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Platform", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Best For", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Key Features", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("x64dbg / x32dbg", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Windows", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Windows malware, crackmes, general RE", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Open source, plugin system (ScyllaHide), excellent UI, active community", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("WinDbg (Preview)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Windows", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Kernel debugging, crash dump analysis, driver RE", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Microsoft official, kernel-mode support, time-travel debugging (TTD)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("GDB + pwndbg / peda", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Linux/macOS", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Linux binaries, exploit development, CTF challenges", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("pwndbg adds heap visualization, ROP gadgets, PEDA adds exploit pattern tools", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("LLDB", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("macOS/iOS/Linux", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Apple platform RE, Swift/ObjC binaries", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Native Apple debugger, Python scripting, Xcode integration", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("OllyDbg", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Windows (32-bit)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Legacy 32-bit Windows RE, learning debugger fundamentals", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Classic tool, many tutorials available, good for learning", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(dbg_data, [1.15*inch, 0.9*inch, 1.6*inch, 2.65*inch]))

    st.append(Paragraph("4.3  Dynamic Analysis & Sandboxes", s['section']))
    dyn_data = [
        [Paragraph("Tool", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("What It Does", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Output", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Any.run", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Interactive online sandbox; run malware and watch execution in real time", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Behavioral reports, network PCAP, process tree, screenshots", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Cuckoo Sandbox", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Self-hosted automated malware analysis framework", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("API calls, registry changes, network traffic, dropped files", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Process Monitor (ProcMon)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Real-time monitoring of filesystem, registry, and process activity on Windows", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Detailed event log with filtering; essential for Windows malware analysis", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Frida", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Dynamic instrumentation toolkit; inject JavaScript into running processes", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Function hooking, argument tracing, memory patching — works on all platforms", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("DynamoRIO / PIN", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Binary instrumentation frameworks for instruction-level tracing", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Execution traces, taint analysis, coverage data for fuzzing", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(dyn_data, [1.4*inch, 2.8*inch, 2.1*inch]))
    st.append(PageBreak())

    st.append(Paragraph("4.4  Network Analysis Tools", s['section']))
    net_data = [
        [Paragraph("Tool", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Function", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Key Capability", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Wireshark", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Packet capture & protocol analysis", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Decode 1000+ protocols; follow TCP streams; export objects from HTTP/FTP", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Burp Suite", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Web application proxy & scanner", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Intercept/modify HTTP/S; fuzz parameters; identify web vulns; essential for web app RE", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Zeek (Bro)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Network traffic analysis framework", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Generate structured logs from PCAP; excellent for C2 traffic analysis at scale", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Scapy", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Python packet manipulation library", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Craft custom packets to test protocols; replay captures; RE network protocols", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Fakenet-NG / INetSim", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Network simulation for malware analysis", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Simulate DNS, HTTP, SMTP etc. to capture malware network behavior without real connectivity", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(net_data, [1.35*inch, 1.85*inch, 3.1*inch]))

    st.append(Paragraph("4.5  Hex Editors & Binary Analysis", s['section']))
    hex_data = [
        [Paragraph("Tool", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Purpose", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("HxD (Windows)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Fast, free hex editor; inspect and patch binary files at the byte level", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("010 Editor", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Template-based hex editor; binary templates for PE/ELF/ZIP/etc. let you parse structures visually", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("ImHex", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Modern open-source hex editor with pattern language, data inspector, and entropy visualizer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Binwalk", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Firmware analysis tool; scans binary files for embedded file signatures, compressed data, and filesystems", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("strings / floss", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Extract printable strings from binaries; FLOSS also decodes obfuscated/stacked strings in malware", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(hex_data, [1.55*inch, 4.75*inch]))

    st.append(Paragraph("4.6  Specialized & Bonus Tools", s['section']))
    spec_items = [
        ("angr", "Python framework for symbolic execution and automated binary analysis — find vulnerabilities without running the code."),
        ("QEMU", "Full-system emulator; run ARM/MIPS/PowerPC binaries on x86 — essential for IoT/firmware RE."),
        ("apktool / jadx", "Android RE: apktool decodes APKs and smali bytecode; jadx decompiles DEX to readable Java."),
        ("objection", "Runtime mobile exploration powered by Frida; bypasses jailbreak/root detection, traces calls."),
        ("Volatility 3", "Memory forensics framework; extract processes, network connections, registry, and malware from RAM dumps."),
        ("YARA", "Write patterns (rules) to classify and hunt for malware families across large file collections."),
        ("PE-bear / CFF Explorer", "Windows PE file analysis tools; inspect headers, sections, imports/exports, rich header."),
        ("VirusTotal", "Upload samples for multi-engine AV scanning plus behavioral reports; use for quick triage."),
    ]
    for tool, desc in spec_items:
        st.append(Paragraph(f"<b><font color='#00FF88'>▸ {tool}:</font></b>  {desc}", s['bullet']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 5 — STATIC ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("5. Static Analysis — Step-by-Step", s['chapter']))
    st.append(hr(s))
    st.append(Paragraph(
        "Static analysis examines a binary without executing it. This is the safest first "
        "approach to any unknown sample. Follow this workflow:", s['body']))

    st.append(Paragraph("5.1  Step 1 — Initial Reconnaissance (Triage)", s['section']))
    triage_steps = [
        ("Identify the file type", "Run `file malware.bin` (Linux) or check magic bytes in a hex editor. Never trust the file extension alone."),
        ("Hash the sample", "Compute MD5, SHA1, SHA256 with `sha256sum`. Search hashes on VirusTotal and MalwareBazaar for instant context."),
        ("Check entropy", "High entropy (>7.0) sections suggest packing/encryption. Use binwalk -E or IDA's entropy plugin. Packed samples need unpacking first."),
        ("Extract strings", "Run `floss malware.exe` — get URLs, IP addresses, registry keys, error messages, and decoded obfuscated strings in one shot."),
        ("Scan for signatures", "Run the binary through YARA rules (e.g., from the YARA-Rules GitHub repo) to instantly classify known malware families."),
        ("Check PE/ELF headers", "Open in PE-bear or CFF Explorer. Look for suspicious section names (.upx, .ndata), abnormal number of imports, or corrupted headers."),
    ]
    for i, (title, desc) in enumerate(triage_steps, 1):
        st.append(Paragraph(f"<b><font color='#FFD700'>Step {i}:</font></b>  <b>{title}</b> — {desc}", s['bullet']))

    st.append(Paragraph("5.2  Step 2 — Disassembly Workflow in Ghidra", s['section']))
    ghidra_steps = [
        "Launch Ghidra → New Project → Non-Shared → Import binary (drag & drop).",
        "Double-click the imported file → click 'Yes' to auto-analyze. Use default analyzers + enable 'Decompiler Parameter ID'.",
        "Wait for analysis. Open the Symbol Tree: Functions → look for 'main', 'WinMain', or DllMain as entry points.",
        "In the Listing view, press 'G' to go to a specific address. Use 'Ctrl+Shift+F' to search for strings you found with FLOSS.",
        "Right-click functions → Rename (press 'L') as you understand them: sub_401000 → decrypt_config.",
        "Use the Call Graph (Graph → Show Call Graph) to visualize which functions call which. Follow execution from entry point.",
        "Use the Decompiler window (Window → Decompiler) for C-like pseudocode. This dramatically accelerates analysis.",
        "Document findings in comments ('Semicolon' key inline, or '//' in decompiler view).",
    ]
    for i, step in enumerate(ghidra_steps, 1):
        st.append(Paragraph(f"<b><font color='#00BFFF'>{i}.</font></b>  {step}", s['bullet']))

    st.append(Paragraph("5.3  Step 3 — Import/Export & IAT Analysis", s['section']))
    st.append(Paragraph(
        "The Import Address Table (IAT) of a PE binary reveals a huge amount about its "
        "capabilities even before reading a single instruction:", s['body']))
    iat_data = [
        [Paragraph("API Call", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Implied Capability", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("CreateRemoteThread, VirtualAllocEx", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Process injection — code being injected into another process", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("RegSetValueEx, RegOpenKeyEx", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Registry persistence — malware writing run keys to survive reboot", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("InternetOpenUrl, HttpSendRequest", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("C2 communication — making HTTP requests to a command & control server", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("CryptEncrypt, CryptGenKey", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Cryptographic operations — possibly ransomware encryption", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("GetAsyncKeyState, SetWindowsHookEx", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Keylogging / input capture — credential theft behavior", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(iat_data, [2.3*inch, 4.0*inch]))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 6 — DYNAMIC ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("6. Dynamic Analysis — Step-by-Step", s['chapter']))
    st.append(hr(s))
    st.append(Paragraph(
        "Dynamic analysis runs the target binary in a controlled environment, observing "
        "its behavior in real time. It reveals runtime-only information: decrypted strings, "
        "network C2 addresses, dropped payloads, and anti-analysis checks.", s['body']))

    st.append(Paragraph("6.1  Setting Up a Safe Lab Environment", s['section']))
    st.append(Paragraph(
        "<b><font color='#FF4444'>⚠ NEVER run malware on your host machine.</font></b>  "
        "Use an isolated virtual machine. Here is the minimum recommended lab setup:", s['body']))
    lab_steps = [
        "Install VMware Workstation Pro or VirtualBox on your analysis machine.",
        "Create a Windows 10 VM (most malware targets Windows). Allocate 4GB RAM, 60GB disk.",
        "Install analysis tools inside the VM: x64dbg, ProcMon, Wireshark, FakeNet-NG, PE-bear.",
        "Take a 'clean' snapshot BEFORE any analysis — this is your restore point.",
        "Configure the VM network to 'Host-Only' or run FakeNet-NG to simulate internet WITHOUT real connectivity.",
        "Install FlareVM (Mandiant's free Windows RE toolkit) — it automates tool installation with one script.",
        "For Linux analysis, use REMnux (reverse engineering Linux distro) as a companion VM.",
        "Disable VMware/VirtualBox guest additions or hide VM artifacts — some malware detects virtualization and changes behavior.",
    ]
    for i, step in enumerate(lab_steps, 1):
        st.append(Paragraph(f"<b><font color='#FFD700'>{i}.</font></b>  {step}", s['bullet']))

    st.append(Paragraph("6.2  Debugging a Binary with x64dbg — Full Workflow", s['section']))
    dbg_steps = [
        ("Open the binary", "Drag the sample onto x64dbg. It pauses at the system breakpoint (ntdll entry). Press F9 to run to the program's entry point."),
        ("Set breakpoints", "Right-click → 'Follow in Disassembler' for interesting functions. Press F2 to toggle a software breakpoint. Set breakpoints on APIs identified in the IAT (e.g., right-click the import → 'Set Breakpoint')."),
        ("Step through code", "F7 = Step Into (follows calls), F8 = Step Over (executes calls without entering), F9 = Run until next breakpoint."),
        ("Inspect memory", "In the dump pane, right-click register values (e.g., EAX pointing to a buffer) → 'Follow in Dump'. Watch encrypted data transform into plaintext."),
        ("Patch instructions", "To bypass checks: double-click an instruction in the disassembly → modify it. Change conditional jumps (JZ/JNZ) to NOP or unconditional JMP to alter flow."),
        ("Dump unpacked code", "If the binary decrypts a payload into memory, use Scylla (x64dbg plugin: Plugins → Scylla) to dump the unpacked PE from memory and fix the IAT."),
    ]
    for i, (title, desc) in enumerate(dbg_steps, 1):
        st.append(Paragraph(f"<b><font color='#00BFFF'>Step {i} — {title}:</font></b>  {desc}", s['bullet']))

    st.append(Paragraph("6.3  API Monitoring with Frida", s['section']))
    st.append(Paragraph("Frida lets you hook any function in a running process with JavaScript — no recompilation needed:", s['body']))
    frida_code = [
        ("# Install Frida",                        ""),
        ("pip install frida-tools",                 ""),
        ("",                                        ""),
        ("# List running processes",                ""),
        ("frida-ps -U",                             "  # -U for USB device (mobile), omit for local"),
        ("",                                        ""),
        ("# Hook a function (JavaScript snippet)",  ""),
        ("frida -p <PID> -e \"",                    ""),
        ("  Interceptor.attach(Module.getExportByName('kernel32.dll', 'CreateFileW'), {", ""),
        ("    onEnter: function(args) {",            ""),
        ("      console.log('CreateFile:', args[0].readUtf16String());", "  // Log filename"),
        ("    }",                                   ""),
        ("  });",                                   ""),
        ("\"",                                      ""),
    ]
    for code, comment in frida_code:
        if code.startswith("#"):
            st.append(Paragraph(code + comment, s['code_comment']))
        else:
            st.append(Paragraph(code + comment, s['code']))

    st.append(Paragraph("6.4  Memory Forensics with Volatility 3", s['section']))
    st.append(Paragraph(
        "When you cannot run a debugger (e.g., analyzing a live incident or a full memory "
        "dump), Volatility 3 extracts forensic artifacts directly from RAM images:", s['body']))
    vol_commands = [
        ("python vol.py -f memory.dmp windows.pslist",         "# List all running processes"),
        ("python vol.py -f memory.dmp windows.pstree",         "# Process tree (shows parent-child relationships)"),
        ("python vol.py -f memory.dmp windows.netscan",        "# Active network connections"),
        ("python vol.py -f memory.dmp windows.malfind",        "# Find injected/suspicious memory regions"),
        ("python vol.py -f memory.dmp windows.dumpfiles --pid 1234", "# Dump files for a specific PID"),
        ("python vol.py -f memory.dmp windows.cmdline",        "# Command-line args for each process"),
    ]
    for cmd, comment in vol_commands:
        st.append(Paragraph(f"{cmd:<55}{comment}", s['code']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 7 — MALWARE ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("7. Malware Analysis Deep Dive", s['chapter']))
    st.append(hr(s))

    st.append(Paragraph("7.1  Malware Classification", s['section']))
    mal_data = [
        [Paragraph("Type", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Primary Behavior", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Key RE Focus", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Ransomware", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Encrypts files and demands ransom; typically uses AES+RSA hybrid encryption", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Find encryption key generation, C2 for key escrow, file enumeration logic", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("RAT (Remote Access Trojan)", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Provides attacker full control: keylogging, screenshots, file access, webcam", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Reverse C2 protocol, extract hard-coded C2 address, decode config", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Rootkit", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Hides its presence by subverting OS structures (SSDT hooks, DKOM, bootkit)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Analyze kernel-mode components; use WinDbg kernel debugging; check DKOM artifacts", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Botnet Agent", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Receives commands from C2 for DDoS, spam, cryptomining, lateral movement", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Decode C2 protocol (often HTTP/IRC/P2P), extract bot ID generation, decode commands", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Stealer", ParagraphStyle('x', textColor=RED_WARN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Exfiltrates credentials, cookies, crypto wallets, browser data", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Find targeted file paths, data exfiltration method (HTTP POST/SMTP), C2 endpoint", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(mal_data, [1.2*inch, 2.4*inch, 2.7*inch]))

    st.append(Paragraph("7.2  Unpacking & Deobfuscation", s['section']))
    st.append(Paragraph(
        "Most real-world malware is packed — the original code is compressed or encrypted, "
        "and a stub decrypts/decompresses it at runtime. Recognizing packing is essential:", s['body']))
    unpack_steps = [
        ("Detect packing", "High entropy in sections + few meaningful imports (only LoadLibrary/GetProcAddress) = packed. Tools: Detect-It-Easy (DIE), PEiD, ExeinfoPE identify the specific packer."),
        ("Generic unpacking", "For UPX (most common packer): simply run `upx -d malware.exe`. For custom packers: set a breakpoint on the OEP (Original Entry Point) — run until memory is decrypted, then dump with Scylla."),
        ("Find the OEP", "Common technique: set hardware breakpoint on execute at the stack pointer value at program start. The packer will jump to OEP after decryption. Alternatively, look for the 'tail jump' (JMP to a very different address after decryption loop)."),
        ("String deobfuscation", "Use FLOSS for static decoding. For runtime decoding: set breakpoint after decryption function, inspect memory at the output buffer."),
        ("Script deobfuscation", "For PowerShell/JS/VBScript droppers: replace the execution call with Write-Output or console.log to dump decoded payload without running it."),
    ]
    for i, (title, desc) in enumerate(unpack_steps, 1):
        st.append(Paragraph(f"<b><font color='#00BFFF'>{i}. {title}:</font></b>  {desc}", s['bullet']))

    st.append(Paragraph("7.3  C2 Infrastructure Mapping", s['section']))
    st.append(Paragraph(
        "Mapping the command-and-control infrastructure is a high-value output of malware RE. "
        "Once you extract a C2 IP or domain, you can build detection rules and pivot to "
        "discover the entire campaign infrastructure:", s['body']))
    c2_steps = [
        "Extract C2 address from decoded config or strings — look for IP literals, DGA seeds, or encoded domains.",
        "Use passive DNS (VirusTotal, Shodan, RiskIQ/PassiveTotal) to find all domains resolving to the same IP.",
        "Run `whois` and certificate transparency (crt.sh) searches to find related infrastructure.",
        "Analyze the C2 communication protocol: what HTTP user-agent does it use? What endpoints? What data format (JSON/custom binary)?",
        "Write Suricata/Snort rules or YARA rules to detect C2 beacons on the network.",
        "Submit findings to ThreatFox (abuse.ch) or ISACs to share IoCs with the broader community.",
    ]
    for i, step in enumerate(c2_steps, 1):
        st.append(Paragraph(f"<b><font color='#FFD700'>{i}.</font></b>  {step}", s['bullet']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 8 — VULNERABILITY RESEARCH
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("8. Vulnerability Research", s['chapter']))
    st.append(hr(s))

    st.append(Paragraph("8.1  Fuzzing Techniques", s['section']))
    st.append(Paragraph(
        "Fuzzing (fuzz testing) automatically generates malformed or random input to find "
        "crashes that indicate vulnerabilities. It is the most scalable method for finding "
        "bugs in closed-source software.", s['body']))
    fuzz_data = [
        [Paragraph("Fuzzer", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Type", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Best For", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("AFL++ (American Fuzzy Lop)", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Coverage-guided grey-box fuzzer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Linux binaries with source code; state-of-the-art mutation strategies", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("WinAFL", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Coverage-guided fuzzer (Windows)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Closed-source Windows applications using DynamoRIO for coverage", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("libFuzzer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("In-process coverage-guided fuzzer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Library fuzzing; fast due to in-process execution; integrates with AddressSanitizer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Boofuzz", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Protocol-aware network fuzzer", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Network protocols and services; successor to Sulley", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(fuzz_data, [1.5*inch, 1.8*inch, 3.0*inch]))

    st.append(Paragraph("8.2  Identifying Memory Corruption Bugs", s['section']))
    vuln_types = [
        ("Buffer Overflow (Stack)", "Local buffer written beyond its size, overwriting the return address. In 64-bit systems, DEP/ASLR/stack canaries are defenses; look for missing canaries (-fno-stack-protector)."),
        ("Heap Overflow", "Heap chunk metadata or adjacent chunks corrupted by out-of-bounds write. Leads to heap metadata exploitation or UAF."),
        ("Use-After-Free (UAF)", "Memory accessed after being freed — if attacker can control re-allocation, they control execution. Very common in browser exploits."),
        ("Format String", "User-controlled format string passed to printf family — allows arbitrary read/write. Look for `printf(user_input)` patterns."),
        ("Integer Overflow", "Arithmetic overflow in size calculations leads to undersized buffer allocation, then overflow. Common in file parsers."),
        ("Type Confusion", "Object treated as wrong type — common in C++ vtable manipulation and JavaScript JIT engines."),
    ]
    for vtype, desc in vuln_types:
        st.append(Paragraph(f"<b><font color='#FF4444'>▸ {vtype}:</font></b>  {desc}", s['bullet']))

    st.append(Paragraph("8.3  Writing a Proof-of-Concept Exploit", s['section']))
    st.append(Paragraph(
        "A PoC exploit demonstrates that a vulnerability is exploitable. For a classic "
        "stack buffer overflow on 64-bit Linux:", s['body']))
    poc_steps = [
        ("Find the offset", "Use `pattern_create` (pwndbg) or `cyclic 200` (pwntools) to generate a De Bruijn sequence. Run the target with this input and note the value of RIP at crash. Run `cyclic -l <RIP value>` to find exact offset."),
        ("Bypass DEP/NX", "Find ROP gadgets with ROPgadget or ropper: `ROPgadget --binary vuln --rop`. Chain gadgets to call mprotect() or use ret2libc to call system('/bin/sh')."),
        ("Bypass ASLR", "Leak a pointer (format string bug, info leak) to defeat ASLR. Alternatively, use partial overwrites or brute-force if entropy is low (32-bit)."),
        ("Write the PoC", "Use pwntools (Python) to automate: craft payload = padding + ROP chain. `p = process('./vuln'); p.sendline(payload); p.interactive()`."),
        ("Document & Report", "Capture the exploit with screenshots, write a clear bug report with CVSS score, reproduction steps, and impact. Submit via responsible disclosure."),
    ]
    for i, (title, desc) in enumerate(poc_steps, 1):
        st.append(Paragraph(f"<b><font color='#00BFFF'>{i}. {title}:</font></b>  {desc}", s['bullet']))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 9 — ADVANCED TECHNIQUES
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("9. Advanced Techniques", s['chapter']))
    st.append(hr(s))

    st.append(Paragraph("9.1  Anti-Reversing Bypass Techniques", s['section']))
    st.append(Paragraph(
        "Real-world malware and protected software employ anti-reversing tricks to hinder analysis. "
        "Recognizing and defeating these is a key professional skill:", s['body']))
    anti_data = [
        [Paragraph("Technique", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("How It Works", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("How to Bypass", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("IsDebuggerPresent", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Checks PEB.BeingDebugged flag to detect debugger", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("ScyllaHide plugin in x64dbg patches this automatically; or NOP the check", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Timing Checks (RDTSC)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Measures execution time; debuggers slow things down detectably", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Patch RDTSC to return consistent values; use ScyllaHide's timing bypass", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("VM Detection (CPUID, registry)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Checks for VMware registry keys, CPUID hypervisor bit, artifacts like vmtools.exe", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Remove VM artifacts from registry; patch CPUID; use bare-metal analysis for evasive samples", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Code Obfuscation (junk code, opaque predicates)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Inserts meaningless instructions or always-true/false conditions to confuse RE tools", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Use symbolic execution (angr) to prune dead branches; manually identify and NOP junk", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Control Flow Flattening", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Transforms structured code into a dispatcher switch — makes graph analysis hard", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Use D810 (IDA plugin) or angr to de-flatten; trace execution to identify real paths", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(anti_data, [1.5*inch, 2.05*inch, 2.75*inch]))

    st.append(Paragraph("9.2  Firmware & Embedded Systems RE", s['section']))
    st.append(Paragraph(
        "IoT devices and network equipment run firmware — often compressed or encrypted filesystem "
        "images. This is one of the richest areas for vulnerability research:", s['body']))
    fw_steps = [
        "Obtain firmware: download from vendor site, extract from device via UART/JTAG, or capture firmware update traffic.",
        "Run binwalk on the firmware image: `binwalk -eM router_fw.bin` — this recursively extracts and decompresses all embedded filesystems.",
        "Navigate the extracted filesystem. Find the web server binary, config files, and any hardcoded credentials.",
        "Use QEMU for emulation: `qemu-arm-static -L ./squashfs-root ./squashfs-root/usr/bin/httpd` — run ARM binaries on x86.",
        "Open interesting binaries in Ghidra (add the relevant CPU architecture plugin — Ghidra supports MIPS/ARM/PPC out of box).",
        "Look for command injection in web CGI handlers, hardcoded credentials, and unauthenticated endpoints.",
    ]
    for i, step in enumerate(fw_steps, 1):
        st.append(Paragraph(f"<b><font color='#FFD700'>{i}.</font></b>  {step}", s['bullet']))

    st.append(Paragraph("9.3  Android & iOS Reverse Engineering", s['section']))
    st.append(Paragraph(
        "Mobile RE requires platform-specific tools and knowledge of the respective runtimes "
        "(ART/Dalvik for Android, Objective-C/Swift runtime for iOS):", s['body']))
    mobile_data = [
        [Paragraph("Task", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Android Tool & Command", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("iOS Tool & Command", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Decompile app", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("jadx-gui app.apk  (Java decompile)", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Hopper Disassembler / Ghidra", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5))],
        [Paragraph("Decode resources", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("apktool d app.apk  (smali + res)", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("class-dump / dsdump for ObjC headers", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5))],
        [Paragraph("Runtime hooking", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Frida / objection", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Frida / Cycript / FLEX 3", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5))],
        [Paragraph("Bypass root/jailbreak detect", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("objection --gadget 'app' explore → android root disable", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Liberty Lite / objection jailbreak bypass", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5))],
        [Paragraph("Traffic interception", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Burp Suite + user-installed CA cert", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Burp Suite + SSL Kill Switch 2", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5))],
    ]
    st.append(make_table(mobile_data, [1.3*inch, 2.5*inch, 2.5*inch]))

    st.append(Paragraph("9.4  Symbolic Execution with angr", s['section']))
    st.append(Paragraph(
        "Symbolic execution treats program inputs as mathematical symbols, exploring all "
        "possible execution paths. angr can automatically find inputs that reach a target "
        "address (e.g., a 'success' path) — useful for crackmes, license checks, and CTF:", s['body']))
    angr_code = [
        "import angr",
        "proj = angr.Project('./crackme', auto_load_libs=False)",
        "state = proj.factory.entry_state()",
        "simgr = proj.factory.simulation_manager(state)",
        "# Find address of 'Correct!' message, avoid 'Wrong!'",
        "simgr.explore(find=0x401200, avoid=0x401250)",
        "if simgr.found:",
        "    solution = simgr.found[0].posix.dumps(0)  # stdin",
        "    print('Password:', solution)",
    ]
    for line in angr_code:
        style = s['code_comment'] if line.startswith('#') else s['code']
        st.append(Paragraph(line, style))
    st.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 10 — PRO WORKFLOW & CAREER
    # ══════════════════════════════════════════════════════════════════════════
    st.append(Paragraph("10. Building Your Pro Workflow & Career Path", s['chapter']))
    st.append(hr(s))

    st.append(Paragraph("10.1  CTF Challenges & Practice Labs", s['section']))
    st.append(Paragraph(
        "Capture The Flag (CTF) competitions are the best way to practice RE in a legal, "
        "gamified environment. Here are the top platforms to grind:", s['body']))
    ctf_data = [
        [Paragraph("Platform", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Focus", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("URL", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Difficulty", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("pwn.college", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Binary exploitation, RE fundamentals, structured curriculum", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("pwn.college", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Beginner → Advanced", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("crackmes.one", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Pure reverse engineering / crackmes in all languages", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("crackmes.one", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("All levels", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("HackTheBox", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Full machines + dedicated RE & pwn challenges", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("hackthebox.com", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Intermediate → Pro", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("PicoCTF", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Educational CTF with RE, binary exploitation, forensics", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("picoctf.org", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Beginner", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("MalwareBazaar", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Real malware samples for analysis practice (free, legal sandbox)", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("bazaar.abuse.ch", ParagraphStyle('x', textColor=ACCENT2, fontName='Courier', fontSize=8.5)),
         Paragraph("Intermediate → Expert", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(ctf_data, [1.2*inch, 2.1*inch, 1.5*inch, 1.4*inch]))

    st.append(Paragraph("10.2  Certifications & Learning Resources", s['section']))
    cert_items = [
        ("GREM (GIAC Reverse Engineering Malware)", "The gold standard RE certification. Covers static/dynamic analysis, unpacking, and malware behavior analysis. Highly respected by employers."),
        ("OSED (OffSec Exploit Developer)", "Offensive Security's exploit development course and exam — x86 Windows exploitation, SEH, DEP/ASLR bypass, format strings."),
        ("CRTO / CRTE", "Certified Red Team Operator/Expert — includes RE for lateral movement and tool customization in realistic AD environments."),
        ("Malware Analysis Fundamentals (CISA)", "Free online training from the US Cybersecurity agency — excellent for those entering the field."),
        ("'Practical Malware Analysis' (book)", "Sikorski & Honig — THE textbook for malware RE. Read it cover-to-cover."),
        ("OpenSecurityTraining2 (ost2.fyi)", "Free university-level RE courses: Architecture 1001, Malware Dynamic Analysis, Exploits 1003."),
        ("'The Shellcoder's Handbook'", "Deep dive into vulnerability research, exploitation, and shellcode — essential for exploit developers."),
    ]
    for cert, desc in cert_items:
        st.append(Paragraph(f"<b><font color='#FFD700'>▸ {cert}:</font></b>  {desc}", s['bullet']))

    st.append(Paragraph("10.3  Professional Career Roadmap", s['section']))
    st.append(Paragraph(
        "Reverse engineering skills open doors to some of the most impactful and "
        "well-compensated roles in cybersecurity:", s['body']))
    career_data = [
        [Paragraph("Role", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Primary RE Focus", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Employers", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
         Paragraph("Salary Range (USD)", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))],
        [Paragraph("Malware Analyst", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Analyze malicious code for AV vendors, threat intel teams", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("CrowdStrike, Mandiant, ESET, Kaspersky, CISA", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$80k – $160k", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Vulnerability Researcher", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Find and analyze zero-days in software and hardware", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Google Project Zero, NSA, ZDI, Synack, MSRC", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$120k – $300k+", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Exploit Developer", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Write weaponized code exploiting discovered vulnerabilities", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Offensive security firms, government contractors, red teams", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$140k – $400k+", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Threat Intelligence Analyst", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("RE malware to attribute campaigns and build intel products", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("Recorded Future, Mandiant, Palo Alto Unit 42, MITRE", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$90k – $180k", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5))],
        [Paragraph("Reverse Engineer (Defense / Intel)", ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=8.5)),
         Paragraph("Nation-state malware analysis, firmware, hardware security", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("NSA/CISA/DARPA, GCHQ, BAE Systems, Booz Allen", ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5)),
         Paragraph("$100k – $250k+", ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica', fontSize=8.5))],
    ]
    st.append(make_table(career_data, [1.4*inch, 1.7*inch, 1.8*inch, 1.35*inch]))

    # 6-month study plan
    st.append(Spacer(1, 10))
    st.append(Paragraph("Suggested 6-Month Study Roadmap", s['subsection']))
    roadmap = [
        ("Months 1–2",   "Foundation", "Learn x86-64 assembly (OpenSecurityTraining2 Arch1001). Read 'Practical Malware Analysis' Chapters 1-8. Set up FlareVM lab. Complete 20+ beginner crackmes."),
        ("Months 3–4",   "Core Skills", "Master Ghidra and x64dbg (YouTube: OALabs, stacksmashing). Complete 'Practical Malware Analysis' fully. Analyze 10 real malware samples from MalwareBazaar. Join CTF team, do PicoCTF/HTB."),
        ("Months 5–6",   "Specialization", "Pick a focus: malware analysis OR exploit dev. Start GREM or OSED prep. Write 2-3 public malware analysis reports. Contribute to open-source RE projects. Apply for junior positions or internships."),
    ]
    rdm_data = [[Paragraph(p, ParagraphStyle('x', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
                 Paragraph(t, ParagraphStyle('x', textColor=GOLD, fontName='Helvetica-Bold', fontSize=9)),
                 Paragraph(desc, ParagraphStyle('x', textColor=TEXT_MAIN, fontName='Helvetica', fontSize=8.5))]
                for p, t, desc in roadmap]
    st.append(make_table(
        [[Paragraph("Period", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
          Paragraph("Theme", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9)),
          Paragraph("Activities", ParagraphStyle('h', textColor=ACCENT, fontName='Helvetica-Bold', fontSize=9))]] + rdm_data,
        [0.95*inch, 1.1*inch, 4.25*inch]
    ))

    # ── Final note
    st.append(Spacer(1, 14))
    st.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    st.append(Paragraph(
        "This guide is a living document. Reverse engineering is an ever-evolving discipline — "
        "stay current by following researchers on Twitter/X, reading Malware Traffic Analysis, "
        "the Mandiant blog, Project Zero blog, and attending conferences like DEF CON, Black Hat, "
        "and REcon. The best reverse engineers never stop learning.",
        ParagraphStyle('final', fontSize=9, textColor=TEXT_MUTED, fontName='Helvetica-Oblique',
                       alignment=TA_CENTER, leading=14)))
    st.append(Spacer(1, 6))
    st.append(Paragraph(
        "© 2025  |  Reverse Engineering: The Complete Professional Cybersecurity Guide  |  Educational Use Only",
        ParagraphStyle('copy', fontSize=8, textColor=TEXT_MUTED, fontName='Helvetica',
                       alignment=TA_CENTER)))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(st)
    print(f"Done → {OUTPUT}")

build()
