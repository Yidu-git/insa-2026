# Cyber Security Report Writing Guide

> **Classification:** CONFIDENTIAL — Internal Use · Not for external distribution  
> **Version:** 1.0 · 2025

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Types of Security Reports](#2-types-of-security-reports)
3. [Report Structure](#3-report-structure)
4. [How to Write Clearly](#4-how-to-write-clearly)
5. [Documenting Individual Findings](#5-documenting-individual-findings)
6. [Formatting Standards](#6-formatting-standards)
7. [Severity Ratings](#7-severity-ratings)
8. [Executive Summary Template](#8-executive-summary-template)
9. [Communicating Your Findings](#9-communicating-your-findings)
10. [Adapting to Your Audience](#10-adapting-to-your-audience)
11. [Team Collaboration](#11-team-collaboration)
12. [Pre-Delivery Checklist](#12-pre-delivery-checklist)

---

## 1. Introduction

A security report is more than a technical record — it is the primary mechanism by which threats are understood, decisions are made, and organisations are protected. Whether you are documenting an active incident, delivering a penetration test, or communicating risk to leadership, the quality of your writing directly determines the quality of the response.

This guide covers how to write, structure, and format security reports, and how to communicate your findings effectively to both technical and non-technical colleagues.

---

## 2. Types of Security Reports

Different scenarios call for different report formats. Knowing which type you are producing shapes every decision about depth, tone, and structure.

### Incident Response Report
Documents a security incident from detection through containment and recovery. Audience is typically mixed — both technical responders and senior management.

**Key sections:** Timeline, root cause, impact assessment, remediation steps.

### Penetration Test Report
Summarises findings from an authorised simulated attack. Must clearly separate the executive summary from technical findings.

**Key sections:** Scope, methodology, findings with CVSS scores, recommendations.

### Vulnerability Assessment Report
A systematic scan and analysis of known weaknesses. Broader scope than a pen test; focus is on enumeration and prioritisation.

**Key sections:** Asset scope, vulnerability inventory, risk ratings, patch priority list.

### Threat Intelligence Report
Contextual analysis of threat actors, TTPs, and indicators of compromise (IoCs). Often shared with peers or leadership.

**Key sections:** Threat actor profile, IoCs, MITRE ATT&CK mapping, recommended detections.

### Compliance / Audit Report
Maps organisational controls against a framework (ISO 27001, SOC 2, NIST, CIS). Identifies gaps and non-conformances.

**Key sections:** Framework overview, control assessments, gap analysis, remediation roadmap.

### Security Posture Report
A recurring (often monthly/quarterly) summary of the organisation's overall security health for leadership or the board.

**Key sections:** KPI dashboard, risk trend, open findings, upcoming priorities.

---

## 3. Report Structure

Regardless of report type, all professional security reports follow a similar hierarchical structure. Each layer serves a different audience.

### 1. Cover Page & Document Control
Report title, classification (CONFIDENTIAL / TLP:RED), date, version number, author, reviewer, and distribution list. Never skip version control — reports are living documents.

### 2. Executive Summary
1–2 pages written for **non-technical decision-makers**. Summarises what happened or was found, the business impact, and the top 3–5 recommended actions. Write this last — once you know the full picture.

### 3. Scope & Methodology
Defines what was included (and excluded), the timeframe, tools used, and testing approach. Sets expectations and limits liability. Be explicit about constraints — limited scope does not mean limited risk.

### 4. Findings
The technical core of the report. Each finding gets its own structured entry with a severity rating, description, evidence, business impact, and recommendations. Ordered by severity (Critical → Informational).

### 5. Risk Summary
A consolidated view of all findings — often a risk matrix or table. Helps stakeholders see the aggregate risk picture at a glance and prioritise remediation effort.

### 6. Recommendations
Concrete, actionable steps with clear ownership, timeframes, and expected outcomes. Distinguish between **immediate** (fix now), **short-term** (30–90 days), and **strategic** (6–12 months) actions.

### 7. Appendices
Raw data, full tool output, scan logs, screenshots, IoC lists, CVE references. Keep the main body readable by pushing raw evidence here. Always label and reference appendices clearly from the relevant finding.

---

## 4. How to Write Clearly

Security writing has one primary rule: **every sentence should help the reader act.** Precision, brevity, and evidence are your tools.

**01 — Know your primary audience before you write**  
Ask: who will act on this? If it's a CISO deciding on budget, lead with business impact. If it's a sysadmin patching systems, lead with technical steps. One report often needs sections written for multiple audiences at different levels of detail.

**02 — Use the active voice**  
Active writing is clearer and assigns ownership. "An attacker can execute arbitrary code" is better than "Arbitrary code execution may be possible via this vector." Own the statement.

**03 — Be precise — avoid weasel words**  
Words like *may*, *could*, *potentially*, and *possibly* erode credibility. If you reproduced a finding, say so. If it's theoretical, state the exact conditions required. Ambiguous findings lead to no remediation.

**04 — Every claim needs evidence**  
Do not state a vulnerability exists without proof. Include a screenshot, output snippet, or reference. Readers — especially sceptical ones — need to verify your findings independently.

**05 — Separate description from impact from recommendation**  
These are three different things. "What is the issue?" (technical description), "Why does it matter?" (business/data impact), and "What should be done?" (remediation) each deserve their own paragraph or field.

**06 — Write recommendations as commands**  
Use imperative verbs. "Patch Apache to version 2.4.58 or later" is actionable. "Patching should be considered" is not. Include the expected outcome: "This will eliminate the known exploit path for CVE-2024-XXXX."

> 💡 **Tip:** Write your executive summary after completing every other section. You cannot summarise what you haven't fully documented yet.

### Language: Do's and Don'ts

| ✅ DO                                                   | ❌ DON'T                                           |
| ------------------------------------------------------ | ------------------------------------------------- |
| Use specific version numbers and CVE IDs               | Use alarming language without supporting evidence |
| Quantify impact where possible                         | Copy-paste scanner output without analysis        |
| Define acronyms at first use                           | Use different names for the same thing            |
| Use consistent terminology throughout                  | Include findings you cannot reproduce             |
| State assumptions and limitations explicitly           | Assign blame by name to individuals               |
| Write past tense for events, present for current state | Leave a finding without a recommendation          |

---

## 5. Documenting Individual Findings

Each finding should be self-contained — a reader should be able to understand, verify, and act on it without reading the rest of the report. Use a consistent template for every finding.

### Finding Template

```
FINDING-001  ─────────────────────────────────────────────

Title:          SQL Injection in Login Endpoint
Severity:       CRITICAL (CVSS 9.8)
CVE Reference:  N/A (Custom Application)
Affected Asset: https://app.example.com/api/v2/login
Status:         Open / Unpatched

DESCRIPTION
The login endpoint at /api/v2/login does not sanitise user-supplied
input in the `username` parameter. Submitting a crafted payload
bypasses authentication controls entirely.

EVIDENCE
The following payload was submitted during testing:

  username=admin'--&password=test

HTTP 200 was returned with a valid session token for the `admin`
account. See Appendix A, Screenshot A-01 for the full response.

BUSINESS IMPACT
An unauthenticated remote attacker can gain administrative access
to the application, exposing all 12,400 user records and all
backend configuration data.

RECOMMENDATION
Immediately implement parameterised queries (prepared statements)
for all database interactions. Apply input validation using an
allow-list approach. Review all other endpoints for the same
pattern. Deploy a WAF rule as an interim measure.

Fix Timeframe:  Immediate (within 48 hours)
Effort:         Medium (2–4 developer days)
```

> ⚠️ **Important:** Never include working exploit code in the main report. Reference it by appendix or provide it through a separate, restricted channel. The report may be shared more broadly than intended.

---

## 6. Formatting Standards

Consistent formatting signals professionalism, improves readability, and makes reports easier to update and compare across engagements.

| Element | Standard Practice | Notes |
|---|---|---|
| Document Classification | Header/footer on every page; use TLP or internal labels | TLP:RED, TLP:AMBER, TLP:GREEN, or CONFIDENTIAL |
| Page Numbering | "Page X of Y" in footer | Prevents confusion if pages are printed out of order |
| Version Control | Version table on page 2 with date, author, and change summary | v0.1 = draft, v1.0 = final, v1.1 = minor update |
| Font | One body font (e.g., Calibri 11pt), one mono font for code | Avoid decorative fonts; optimise for readability |
| Headings | Three levels maximum: H1, H2, H3 | Deep nesting creates confusion; reorganise instead |
| Tables | Use for comparisons, risk summaries, and finding inventories | Include column headers; stripe rows for long tables |
| Screenshots | Annotate with arrows/boxes; caption every image | Crop out irrelevant UI; redact sensitive tokens |
| Code / Commands | Always use a monospace block with syntax highlighting | Never embed commands inline in body text |
| Hyperlinks | Descriptive text, not raw URLs in running prose | Include full URLs in references/footnotes |

### Naming Conventions

- Use consistent asset identifiers (IP, hostname, or system name — pick one and stick to it)
- Name findings with an ID prefix: `FIND-001`, `VULN-003`
- Reference appendices clearly: "See Appendix B"
- Date format: ISO 8601 — `2025-03-14`

### File Naming

```
ClientName_ReportType_YYYY-MM-DD_v1.0.pdf
```

- Always deliver as **PDF** for final distribution
- Keep the editable source (DOCX/Markdown) under version control
- Never send a report as a `.docx` to external parties

> 🔒 **Classification reminder:** All security reports containing system details, vulnerabilities, or internal network information must be classified at minimum as CONFIDENTIAL or TLP:AMBER. Treat draft reports with the same care as final ones.

---

## 7. Severity Ratings

Severity ratings help stakeholders triage findings. Use the **CVSS v3.1 scale** for scored findings, or a consistent qualitative scheme when CVSS isn't applicable.

| Rating              | CVSS Score | Description                                           |
| ------------------- | ---------- | ----------------------------------------------------- |
| 🔴 **Critical**     | 9.0–10.0   | Immediate exploitation likely; severe business impact |
| 🟠 **High**         | 7.0–8.9    | Significant risk; should be remediated urgently       |
| 🟡 **Medium**       | 4.0–6.9    | Moderate risk; remediate in the short term            |
| 🔵 **Low**          | 0.1–3.9    | Minor risk; remediate as part of regular maintenance  |
| ⚪ **Informational** | 0.0        | No direct risk; noted for awareness or best practice  |

### When to Use CVSS

Use CVSS for:
- Software vulnerabilities with a known exploit path
- CVE-tracked issues in commercial or open-source software
- Network, web application, and API vulnerabilities

Use the NVD CVSS calculator to justify your base score and always document which metrics you selected.

### Qualitative Ratings (No CVSS)

Use qualitative ratings for:
- Policy / process gaps without a direct technical path
- Governance, risk, and compliance (GRC) findings
- Social engineering and physical security observations

State your rating rationale explicitly. Consider **Likelihood × Impact** as a guide.

> 💡 **Context matters:** A medium CVSS-scored vulnerability in a public-facing endpoint may present higher actual business risk than a high-scored finding on an air-gapped internal system. Always document contextual factors that elevate or reduce the risk beyond the base score.

---

## 8. Executive Summary Template

The executive summary is the most-read section of any report. Executives may read only this page. Make every word count.

```
EXECUTIVE SUMMARY
─────────────────────────────────────────────────────────

ENGAGEMENT OVERVIEW
Between [START DATE] and [END DATE], [Company/Team] conducted a
[type of assessment] of [scope]. The assessment was authorised
by [name/role] under [reference / statement of work].

KEY FINDINGS
The assessment identified [N] Critical, [N] High,
[N] Medium, and [N] Low severity findings.

The most significant risks identified were:

  1. [Finding title] — [One-sentence business impact]
  2. [Finding title] — [One-sentence business impact]
  3. [Finding title] — [One-sentence business impact]

BUSINESS IMPACT
The most critical findings, if exploited, could result in
[consequence: data breach / service disruption / regulatory
penalty / financial loss]. [Specific affected systems or
data types].

RECOMMENDED IMMEDIATE ACTIONS
  1. [Action] — Owner: [Team/Role] — Due: [Timeframe]
  2. [Action] — Owner: [Team/Role] — Due: [Timeframe]
  3. [Action] — Owner: [Team/Role] — Due: [Timeframe]

Full technical details and remediation guidance are provided
in the body of this report.
─────────────────────────────────────────────────────────
```

---

## 9. Communicating Your Findings

Writing the report is only half the job. How you deliver and discuss findings determines whether they are acted upon. Security findings often represent bad news — communicate them with professionalism, clarity, and a solution-oriented mindset.

### Verbal Briefings & Presentations
When presenting to leadership, lead with business impact and required decisions — not technical methodology. Prepare a slide deck version of the executive summary. Anticipate questions: "What's our exposure?", "Who else knows?", "How long to fix?". Practise concise answers.

### Incident Escalation
During an active incident, verbal or instant-message updates should follow a structured format:

> **What happened → Current status → What we're doing → What we need**

Avoid overloading stakeholders with technical jargon when they need to make decisions. Send written situation reports (SITREPs) at regular intervals.

### Email Communication
Security emails require particular care:

- Use clear subject lines: `[SECURITY - HIGH] Action Required: CVE-XXXX patching by 14 March`
- Never send sensitive findings or credentials in unencrypted email
- Use S/MIME or PGP for external parties, or a secure file-sharing platform
- Keep emails concise; attach the full report rather than summarising in the body

### Notification of Critical Findings
Critical or High findings discovered mid-engagement should be communicated **immediately** — do not wait for the final report.

1. Call or message the designated contact first
2. Follow up in writing with a brief one-page interim notification report
3. Document that you gave this notice and when

---

## 10. Adapting to Your Audience

The same finding needs to be communicated differently depending on who you are speaking to.

| Audience | Focus | Language Level | What They Need |
|---|---|---|---|
| Board / CEO | Business risk & liability | Non-technical | Risk in financial/reputation terms, required decisions, regulatory exposure |
| CISO / CTO | Strategic risk posture | Semi-technical | Overall security posture, resource implications, programme priorities |
| Security Manager | Operational risk & priorities | Technical | Finding details, affected assets, team workload, remediation plans |
| Sysadmin / DevOps | Specific remediation steps | Highly technical | Exact commands, patch versions, config changes, validation steps |
| Developer | Root cause & code-level fix | Highly technical | Vulnerable code snippet, secure alternative pattern, test case to verify fix |
| Legal / Compliance | Regulatory obligations | Non-technical | What data was at risk, notification requirements, evidence chain |

> ✅ **Best practice:** Consider including an "Audience Guide" note at the start of long reports — e.g., "Management readers: please see Section 1 and Section 6. Technical teams: all sections apply."

---

## 11. Team Collaboration

Security reports are rarely produced by one person. Establishing clear norms around collaboration prevents duplication, contradictions, and version confusion.

### Version Control
All drafts should be tracked. Use a shared platform (SharePoint, Confluence, Git) with a clear naming strategy:

```
v0.1-draft-analyst
v0.2-peer-review
v0.3-client-review
v1.0-final
```

### Peer Review
Every finding should be reviewed by at least one other team member before the report is finalised. Look for:
- Accuracy and reproducibility
- Missing evidence
- Inconsistent severity ratings
- Tone and clarity issues

### Responsible Disclosure
- Agree internally on disclosure scope and timing before communicating anything to the client
- Have a single, agreed point of contact for the client
- Avoid multiple team members sending conflicting messages

### Writing for Handover
Reports are often passed to colleagues, remediation teams, or auditors who weren't present. Include:
- **Background:** Why was this assessment conducted?
- **Constraints:** What was out of scope or time-limited?
- **Contact information:** Who to call with questions?
- **Credential/access notes:** What accounts were used during testing? (in a restricted appendix)

### Slack / Chat Communication During Engagements

| ✅ Good Practice | ❌ Avoid |
|---|---|
| Use dedicated, private channels for engagement comms | Sharing credentials or tokens in unencrypted chat |
| Post structured updates: status, blockers, next steps | Posting raw vulnerability details in public channels |
| Link to the shared document rather than pasting findings inline | Informal language that could be misread out of context |
| Tag only people who need to act | Using personal messaging apps for security matters |

---

## 12. Pre-Delivery Checklist

Run through this checklist before sending any security report to a client or stakeholder.

### Content
- [ ] Executive summary is written for non-technical readers
- [ ] All findings have evidence attached or referenced
- [ ] Every finding has a clear, actionable recommendation
- [ ] Severity ratings are consistent and justified
- [ ] Scope and methodology are clearly defined
- [ ] No copy-pasted scanner output without analysis
- [ ] Critical/High findings were notified immediately

### Formatting
- [ ] Classification label on every page
- [ ] Version table updated on page 2
- [ ] All screenshots are annotated and captioned
- [ ] All appendices are referenced in the main body
- [ ] Table of contents is accurate
- [ ] File name follows naming convention
- [ ] Final version exported as PDF

### Review
- [ ] Peer review completed by a second analyst
- [ ] Spell check and grammar review done
- [ ] All system names and IP addresses are accurate
- [ ] Client name and engagement dates are correct
- [ ] No internal comments or tracked changes remain

### Delivery
- [ ] Correct recipient confirmed before sending
- [ ] Encrypted delivery method used (if required)
- [ ] Accompanying cover email is professional and concise
- [ ] Walk-through or debrief session scheduled
- [ ] Retention/destruction policy communicated

---

> 📌 **Remember:** A security report is a professional legal document. It may be used in regulatory proceedings, litigation, or insurance claims. Write accordingly — factually, precisely, and without embellishment or speculation.

---

*Cyber Security Report Writing Guide · v1.0 · 2025*
