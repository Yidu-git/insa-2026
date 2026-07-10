# NexusBank — Presentation Script

  

**Deck:** NexusBank.pptx (10 slides)

**Audience:** Engineering / technical stakeholders

**Goal:** Explain what the project is, what problem it solves, how it's built, and what's left to do.

  

---

  

## Slide 1 — Title

  

**On slide:** NexusBank Backend · From demo toy to real API · Node.js + Express + SQLite

  

**Script:**

"NexusBank started life as a pure front-end demo — a single HTML file simulating a banking app. This presentation walks through the backend we built to make it real: real auth, real data integrity, real security boundaries — while keeping the exact same UI the demo shipped with."

  

---

  

## Slide 2 — What This Project Is

  

**On slide:** A real Node/Express + SQLite API behind the existing NexusBank/NearPay demo UI, with hashed passwords, signed sessions, and server-side validation on every money-moving action.
                
  

**Script:**

"The brief was simple: keep the UI pixel-for-pixel identical, but replace every piece of client-side fakery with a real backend. Same screens, same flows — but now backed by an actual database and actual security."

  

---

  

## Slide 3 — The Problem With the Original Demo

  

**On slide (before/after framing):**

- Passwords stored in plaintext in localStorage

- Anyone could open devtools and edit their own balance

- Two browser tabs could "discover" each other to fake NearPay

- No real backend at all — everything lived in the browser

  

**Script:**

"None of this was handling real money, but none of it was a real system either. Client-side state means client-side trust — and in a banking demo, that's the whole point you're supposed to get right. Every one of these four issues maps directly to a fix in the new backend."

  

---

  

## Slide 4 — Architecture at a Glance

  

**On slide (diagram):** Browser (same HTML/CSS/JS) → Express API (`/api/*`) → SQLite (WAL mode) — single origin, single Node process, cookie-based session flowing through middleware.

  

**Script:**

"It's intentionally a simple, single-origin architecture: one Node process serves both the static frontend and the JSON API, so there's no CORS dance and no separate deploy to coordinate. Express sits in front of a single SQLite database running in WAL mode, which is plenty for a demo or small-scale deployment."

  

---

  

## Slide 5 — Data Model

  

**On slide (table groupings):**

- **Identity:** `users` (bcrypt hash, account number, balance in cents)

- **Money movement:** `transactions`, `loans`, `loan_payments`

- **NearPay:** `presence`, `payment_requests`

- **Device trust:** `devices`, `device_links`

  

**Script:**

"Eight tables, four logical groups. Everything money-related is stored as integer cents, never floats — that one decision eliminates an entire class of rounding bugs. The schema also carries forward-compatible migrations baked in, so older databases pick up new columns and loan transaction types automatically on startup."

  

---

  

## Slide 6 — Security Model

  

**On slide (icon rows):**

- Passwords hashed with bcrypt, 12 rounds

- Sessions are httpOnly, signed JWT cookies — invisible to page JS

- Transfers run inside SQLite transactions — no race-condition overdrafts

- Rate limiting on login/signup to blunt brute force

- Server refuses to boot without a real `JWT_SECRET`

  

**Script:**

"This slide is really the heart of the project. Every one of these closes a specific hole from the original demo. The one I'd call out especially: transfers, deposits, and NearPay payments all run inside atomic SQLite transactions, so two simultaneous transfer requests can't both pass a balance check and overdraw the same account — a classic race condition that's easy to miss in a demo project."

  

---

  

## Slide 7 — API Surface

  

**On slide (grouped table):**

- **Auth:** signup, login, logout, `/me`

- **Bank:** balance summary, transactions, transfer, deposit, recipient lookup

- **NearPay:** presence heartbeat, nearby users, direct pay, payment-request links

- **Loans:** rate table, apply, list, detail + payment history

- **Devices:** list, rename, revoke, QR-code device linking

  

**Script:**

"Five route groups, all authenticated through the same httpOnly cookie — the frontend never touches a token directly, it just sets `credentials: include` and the cookie does the rest. Loans and device management are two feature areas that grew past the original README scope: instant-approval demo loans with amortized payments, and a full device-trust system with QR-code linking and revocation."

  

---

  

## Slide 8 — Feature Deep Dive: NearPay & Loans

  

**On slide (two columns):**

- **NearPay:** server-tracked presence (30s freshness window) replaces the shared-localStorage trick; payment-request links are validated server-side, not DOM-patched

- **Loans:** term-based rate table, amortized monthly payments, instant demo disbursement into balance, full payment history per loan

  

**Script:**

"NearPay's 'nearby devices' feature used to work only because two tabs shared the same localStorage — it looked real but only worked on one machine. Now presence is a real server-side table with a freshness window, so it works across actual separate devices. Loans is a newer addition: pick a term, see the real APR, apply, and the funds land in your balance immediately with a proper amortization schedule tracked payment-by-payment."

  

---

  

## Slide 9 — Deployment

  

**On slide (checklist):**

- Any host that runs `npm install && npm start`

- Required: `JWT_SECRET`, persistent volume via `DATA_DIR`

- Render/Railway: attach a Disk/Volume or the SQLite file gets wiped on every redeploy

- Single origin by default — `ALLOWED_ORIGINS` only needed if frontend is split out

  

**Script:**

"The one deployment trap this project explicitly guards against: SQLite lives on disk, and most container platforms give you an ephemeral filesystem by default. Skip the persistent volume and your entire user base disappears on the next deploy. The README calls this out hard, and the server refuses to start without a JWT secret as a second guardrail."

  

---

  

## Slide 10 — Honest Limitations & Next Steps

  

**On slide (two columns):**

- **What it is:** demo bank, no real money or payment rails, no KYC/AML, NearPay is a presence simulation not real Bluetooth/NFC

- **Natural next steps:** email verification, password reset, 2FA, Postgres if traffic grows past SQLite's comfort zone

  

**Script:**

"To be clear about scope: this is still a demo. No real money moves, there's no compliance layer, and NearPay simulates proximity rather than using real Bluetooth or NFC. But the SQL is simple enough that a future move to Postgres wouldn't be a rewrite — and the natural next features are the obvious ones: verified email, password reset, and two-factor auth. That's a good note to end on and open the floor."

  

---

  

*End of script.*