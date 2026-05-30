const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Blue Teaming & SOC Operations";

// Color palette — dark cybersecurity theme
const C = {
  dark:    "0D1117",
  darker:  "060A0E",
  navy:    "0F2942",
  teal:    "00D4AA",
  tealDim: "00A882",
  blue:    "1E90FF",
  blueDim: "1565C0",
  white:   "FFFFFF",
  light:   "C9D1D9",
  muted:   "8B949E",
  accent:  "F0A500",
  red:     "FF4444",
  green:   "39D353",
  card:    "161B22",
  cardBdr: "21262D",
};

const FONT_HEAD = "Consolas";
const FONT_BODY = "Calibri";

// ─── helpers ────────────────────────────────────────────────────────────────

function titleSlide() {
  const s = pres.addSlide();
  s.background = { color: C.darker };

  // Left accent bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.18, h: 5.625, fill: { color: C.teal } });

  // Decorative circles
  s.addShape(pres.shapes.OVAL, { x: 7.5, y: -0.5, w: 3.5, h: 3.5, fill: { color: C.navy }, line: { color: C.teal, width: 1 } });
  s.addShape(pres.shapes.OVAL, { x: 8.2, y: 2.8, w: 2.2, h: 2.2, fill: { color: C.card }, line: { color: C.blue, width: 1 } });

  s.addText("BLUE TEAMING", { x: 0.5, y: 1.1, w: 7, h: 0.7, fontFace: FONT_HEAD, fontSize: 42, bold: true, color: C.teal, margin: 0 });
  s.addText("& SOC OPERATIONS", { x: 0.5, y: 1.85, w: 7.5, h: 0.7, fontFace: FONT_HEAD, fontSize: 42, bold: true, color: C.white, margin: 0 });
  s.addText("Comprehensive Study Notes", { x: 0.5, y: 2.7, w: 7, h: 0.45, fontFace: FONT_BODY, fontSize: 18, color: C.light, margin: 0 });
  s.addText("Cybersecurity — Defensive Security Operations Reference  |  2025 Edition", {
    x: 0.5, y: 3.3, w: 8, h: 0.35, fontFace: FONT_BODY, fontSize: 12, color: C.muted, margin: 0
  });

  // Sections preview
  const topics = [
    "01  Blue Teaming Fundamentals",
    "02  Types of Logs",
    "03  The 5W1H Framework",
    "04  SOC Analysis",
    "05  Incident Response (IR)",
    "06  Cyber Threat Intelligence",
    "07  How to Analyze a Log",
    "08  Quick Reference",
  ];
  topics.forEach((t, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i % 4;
    s.addText(t, {
      x: 0.5 + col * 4.5, y: 3.9 + row * 0.38, w: 4.2, h: 0.33,
      fontFace: FONT_BODY, fontSize: 10.5, color: i % 2 === 0 ? C.teal : C.light, margin: 0
    });
  });
}

function sectionHeader(num, title, subtitle) {
  const s = pres.addSlide();
  s.background = { color: C.dark };

  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.navy } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.5, w: 10, h: 0.005, fill: { color: C.teal } });

  s.addText(`0${num}`, { x: 0.6, y: 0.7, w: 2, h: 1.5, fontFace: FONT_HEAD, fontSize: 96, bold: true, color: C.teal, transparency: 30, margin: 0 });
  s.addText(title.toUpperCase(), { x: 0.6, y: 2.65, w: 9, h: 0.75, fontFace: FONT_HEAD, fontSize: 34, bold: true, color: C.white, margin: 0 });
  if (subtitle) {
    s.addText(subtitle, { x: 0.6, y: 3.5, w: 9, h: 0.5, fontFace: FONT_BODY, fontSize: 15, color: C.light, margin: 0 });
  }
}

function contentSlide(title, buildFn) {
  const s = pres.addSlide();
  s.background = { color: C.dark };
  // Top bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.55, fill: { color: C.navy } });
  s.addText(title.toUpperCase(), {
    x: 0.35, y: 0, w: 9.3, h: 0.55, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: C.teal, valign: "middle", margin: 0
  });
  buildFn(s);
  return s;
}

function card(s, x, y, w, h, headerText, headerColor, bodyLines) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.32, fill: { color: headerColor || C.navy }, line: { color: headerColor || C.navy, width: 0 } });
  s.addText(headerText, { x: x + 0.12, y, w: w - 0.15, h: 0.32, fontFace: FONT_HEAD, fontSize: 10.5, bold: true, color: C.white, valign: "middle", margin: 0 });
  if (bodyLines && bodyLines.length) {
    const items = bodyLines.map((t, i) => ({
      text: t,
      options: { bullet: true, color: i % 2 === 0 ? C.light : C.muted, fontSize: 9.5, fontFace: FONT_BODY, breakLine: i < bodyLines.length - 1 }
    }));
    s.addText(items, { x: x + 0.1, y: y + 0.36, w: w - 0.2, h: h - 0.44, valign: "top", margin: 0 });
  }
}

function tableSlide(title, headers, rows, colWidths) {
  const s = pres.addSlide();
  s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.55, fill: { color: C.navy } });
  s.addText(title.toUpperCase(), { x: 0.35, y: 0, w: 9.3, h: 0.55, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: C.teal, valign: "middle", margin: 0 });

  const tableData = [
    headers.map(h => ({ text: h, options: { bold: true, color: C.white, fill: { color: C.blueDim }, fontSize: 10, fontFace: FONT_HEAD } })),
    ...rows.map((row, ri) => row.map((cell, ci) => ({
      text: cell,
      options: {
        color: ci === 0 ? C.teal : C.light,
        fill: { color: ri % 2 === 0 ? C.card : C.dark },
        fontSize: 9.5, fontFace: FONT_BODY
      }
    })))
  ];

  s.addTable(tableData, {
    x: 0.35, y: 0.7, w: 9.3, h: 4.7,
    colW: colWidths,
    border: { pt: 0.5, color: C.cardBdr },
    margin: [3, 6, 3, 6]
  });
  return s;
}

// ─── BUILD SLIDES ────────────────────────────────────────────────────────────

// TITLE
titleSlide();

// ── SECTION 1: Blue Teaming Fundamentals ──
sectionHeader(1, "Blue Teaming Fundamentals", "What it is, roles, tools & frameworks");

// 1a — What + Mission
contentSlide("Blue Teaming — Overview", s => {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 0.68, w: 5.6, h: 4.65, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 0.68, w: 5.6, h: 0.32, fill: { color: C.tealDim } });
  s.addText("WHAT IS BLUE TEAMING?", { x: 0.45, y: 0.68, w: 5.4, h: 0.32, fontFace: FONT_HEAD, fontSize: 10.5, bold: true, color: C.white, valign: "middle", margin: 0 });
  s.addText([
    { text: "Blue Teaming is ", options: { color: C.light, fontSize: 11, fontFace: FONT_BODY } },
    { text: "defensive cybersecurity operations", options: { color: C.teal, bold: true, fontSize: 11, fontFace: FONT_BODY } },
    { text: " where a dedicated team protects an organization's systems, networks, and data from both external and internal threats.", options: { color: C.light, fontSize: 11, fontFace: FONT_BODY } },
    { text: "\n\nCore Mission:", options: { color: C.accent, bold: true, fontSize: 11, fontFace: FONT_HEAD, breakLine: true } },
    { text: "\nDetect, prevent, and respond to cyber threats before they cause damage to the organization's assets, data, or reputation.", options: { color: C.light, fontSize: 11, fontFace: FONT_BODY } },
    { text: "\n\nCore Mindset:", options: { color: C.accent, bold: true, fontSize: 11, fontFace: FONT_HEAD, breakLine: true } },
  ], { x: 0.47, y: 1.05, w: 5.35, h: 1.6, valign: "top", margin: 0 });

  const mindset = ["Assuming Breach — attacker may already be inside", "Defense in Depth — layer multiple controls", "Zero Trust — verify every request regardless of source", "Continuous Improvement — learn from incidents"];
  const items = mindset.map((t, i) => ({ text: t, options: { bullet: true, color: i % 2 === 0 ? C.light : C.muted, fontSize: 9.5, fontFace: FONT_BODY, breakLine: i < mindset.length - 1 } }));
  s.addText(items, { x: 0.47, y: 2.75, w: 5.35, h: 1.5, valign: "top", margin: 0 });

  // Team types on right
  const teams = [
    { name: "BLUE TEAM", desc: "Defenders — monitor, detect, respond. Operate 24/7 in the SOC.", color: C.blue },
    { name: "RED TEAM", desc: "Attackers — simulate real-world threat actors via penetration testing.", color: C.red },
    { name: "PURPLE TEAM", desc: "Blue + Red collaboration sharing findings to improve detection.", color: "#9B59B6" },
    { name: "WHITE TEAM", desc: "Administrators in exercises who set rules and evaluate performance.", color: C.muted },
  ];
  teams.forEach((t, i) => {
    const y = 0.68 + i * 1.15;
    s.addShape(pres.shapes.RECTANGLE, { x: 6.2, y, w: 3.45, h: 1.05, fill: { color: C.card }, line: { color: t.color, width: 2 } });
    s.addText(t.name, { x: 6.32, y: y + 0.06, w: 3.2, h: 0.28, fontFace: FONT_HEAD, fontSize: 10.5, bold: true, color: t.color, margin: 0 });
    s.addText(t.desc, { x: 6.32, y: y + 0.36, w: 3.2, h: 0.6, fontFace: FONT_BODY, fontSize: 9, color: C.light, margin: 0 });
  });
});

// 1b — Tools + Frameworks
contentSlide("Key Tools & Frameworks", s => {
  const tools = [
    { name: "SIEM", desc: "Log aggregation, alerting & correlation. Splunk, IBM QRadar, Microsoft Sentinel." },
    { name: "IDS/IPS", desc: "Monitor traffic for malicious patterns. Snort, Suricata." },
    { name: "EDR", desc: "Endpoint threat monitoring. CrowdStrike, Carbon Black." },
    { name: "SOAR", desc: "Automates repetitive SOC tasks and playbooks." },
    { name: "Firewall/WAF", desc: "Filter malicious network and web app traffic." },
    { name: "Threat Intel", desc: "MISP, ThreatConnect for aggregating threat data." },
  ];
  tools.forEach((t, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.35 + col * 3.15;
    const y = 0.7 + row * 1.5;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.0, h: 1.3, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h: 1.3, fill: { color: C.teal } });
    s.addText(t.name, { x: x + 0.16, y: y + 0.08, w: 2.75, h: 0.3, fontFace: FONT_HEAD, fontSize: 12, bold: true, color: C.teal, margin: 0 });
    s.addText(t.desc, { x: x + 0.16, y: y + 0.42, w: 2.75, h: 0.78, fontFace: FONT_BODY, fontSize: 9.5, color: C.light, margin: 0 });
  });

  const fw = ["MITRE ATT&CK — Adversary TTPs knowledge base for mapping attacks", "NIST CSF — Identify, Protect, Detect, Respond, Recover", "CIS Controls — Prioritized security controls for defense", "D3FEND — MITRE framework for defensive techniques", "Cyber Kill Chain — Maps attack stages for early detection"];
  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 3.3, w: 9.3, h: 1.95, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
  s.addText("FRAMEWORKS", { x: 0.47, y: 3.35, w: 3, h: 0.28, fontFace: FONT_HEAD, fontSize: 10, bold: true, color: C.accent, margin: 0 });
  const fwItems = fw.map((t, i) => ({ text: t, options: { bullet: true, color: i % 2 === 0 ? C.light : C.muted, fontSize: 9.5, fontFace: FONT_BODY, breakLine: i < fw.length - 1 } }));
  s.addText(fwItems, { x: 0.47, y: 3.67, w: 9.1, h: 1.5, valign: "top", margin: 0 });
});

// ── SECTION 2: Types of Logs ──
sectionHeader(2, "Types of Logs", "The foundation of all Blue Team visibility");

contentSlide("Log Categories", s => {
  const cats = [
    { title: "SYSTEM LOGS", color: C.blue, items: ["Windows Event Logs (.evtx)", "Linux Syslog /var/log/syslog", "Auth Log /var/log/auth.log", "Key Event IDs: 4624, 4625, 4688, 7045"] },
    { title: "NETWORK LOGS", color: C.teal, items: ["Firewall allow/deny logs", "NetFlow / IPFIX traffic summaries", "DNS query logs (C2 detection)", "DHCP IP-to-device mapping"] },
    { title: "APPLICATION LOGS", color: C.accent, items: ["Web server logs (Apache/Nginx/IIS)", "Database query & login logs", "Email server SMTP logs", "Application error/crash logs"] },
    { title: "SECURITY LOGS", color: "#E74C3C", items: ["SIEM correlated alerts", "EDR/AV detections & quarantine", "WAF attack logs (SQLi, XSS)", "VPN remote access sessions"] },
    { title: "ENDPOINT LOGS", color: "#9B59B6", items: ["Process execution records", "Windows Registry read/write", "PowerShell script block logging", "Sysmon enhanced telemetry"] },
    { title: "CLOUD LOGS", color: "#27AE60", items: ["AWS CloudTrail (API calls)", "Azure Monitor / Activity Log", "GCP Cloud Audit Logs", "Container/Kubernetes events"] },
  ];
  cats.forEach((c, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    card(s, 0.35 + col * 3.15, 0.67 + row * 2.35, 3.0, 2.2, c.title, c.color, c.items);
  });
});

// Key Windows Event IDs table
tableSlide("Critical Windows Event IDs",
  ["Event ID", "Description", "Significance"],
  [
    ["4624", "Successful account logon", "Baseline — watch for unusual logon types/times"],
    ["4625", "Failed account logon", "High frequency = brute force indicator"],
    ["4648", "Logon using explicit credentials", "Indicates Pass the Hash / credential reuse"],
    ["4688", "New process created", "Process execution — watch for unusual parents/paths"],
    ["4698 / 4702", "Scheduled task created/modified", "Common persistence mechanism"],
    ["4719", "System audit policy changed", "Attacker disabling logging"],
    ["7045", "New service installed", "Malware installation / persistence"],
    ["1102", "Security audit log cleared", "Log tampering — high severity"],
    ["4732", "Member added to local security group", "Privilege escalation indicator"],
  ],
  [1.2, 4.5, 3.6]
);

// ── SECTION 3: 5W1H ──
sectionHeader(3, "The 5W1H Framework", "Structured investigation methodology for every alert");

contentSlide("5W1H — Investigation Framework", s => {
  const qs = [
    { q: "WHAT", color: C.teal,   text: "What type of attack? What systems/data affected? What IoCs were observed? What controls detected/failed?" },
    { q: "WHEN", color: C.blue,   text: "When initiated? When detected (MTTD)? Full attack timeline from initial access to exfiltration. Normalize to UTC." },
    { q: "HOW",  color: C.accent, text: "How did attacker gain access? How did they escalate privileges? How did they move laterally? Map to MITRE ATT&CK." },
    { q: "WHERE",color: "#27AE60",text: "Which systems/VLANs compromised? Where geographically did attack originate? Where was data exfiltrated from?" },
    { q: "WHO",  color: "#9B59B6",text: "Who is the threat actor? Which accounts compromised? Who needs to be notified? (CISO, Legal, PR, Regulators)" },
    { q: "WHY",  color: "#E74C3C",text: "Why was this org targeted? Why did the attack succeed? Root cause analysis → corrective actions." },
  ];
  qs.forEach((q, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.35 + col * 3.15;
    const y = 0.67 + row * 2.35;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.0, h: 2.2, fill: { color: C.card }, line: { color: q.color, width: 2 } });
    s.addText(q.q, { x: x + 0.12, y: y + 0.08, w: 2.7, h: 0.55, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: q.color, margin: 0 });
    s.addText(q.text, { x: x + 0.12, y: y + 0.72, w: 2.75, h: 1.38, fontFace: FONT_BODY, fontSize: 9.5, color: C.light, margin: 0 });
  });
});

// ── SECTION 4: SOC Analysis ──
sectionHeader(4, "SOC Analysis", "Triage workflow, analyst tiers, metrics & SIEM");

// Analyst Tiers
contentSlide("SOC Analyst Tiers & Workflow", s => {
  // Tiers
  const tiers = [
    { tier: "TIER 1", role: "Alert Analyst", color: C.green, desc: "First-line triage. Review SIEM/EDR alerts. Determine true positive, false positive, or escalate. High volume, repetitive work." },
    { tier: "TIER 2", role: "Incident Responder", color: C.blue, desc: "Deep-dive investigation of escalated incidents. Correlate logs, identify attack scope, contain threats." },
    { tier: "TIER 3", role: "Threat Hunter", color: C.accent, desc: "Proactively hunt for threats not caught by automated tools. Develop detection content. Reverse engineer malware." },
    { tier: "SOC MGR", role: "Manager", color: C.muted, desc: "Oversee operations, SLA compliance, metrics, vendor relations, and CISO reporting." },
  ];
  tiers.forEach((t, i) => {
    const y = 0.67 + i * 1.12;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y, w: 0.55, h: 1.0, fill: { color: t.color } });
    s.addText(t.tier, { x: 0.35, y: y + 0.3, w: 0.55, h: 0.4, fontFace: FONT_HEAD, fontSize: 7.5, bold: true, color: C.dark, align: "center", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.9, y, w: 4.15, h: 1.0, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
    s.addText(t.role, { x: 1.02, y: y + 0.06, w: 3.9, h: 0.28, fontFace: FONT_HEAD, fontSize: 11, bold: true, color: t.color, margin: 0 });
    s.addText(t.desc, { x: 1.02, y: y + 0.36, w: 3.9, h: 0.56, fontFace: FONT_BODY, fontSize: 9, color: C.light, margin: 0 });
  });

  // Metrics
  const metrics = [
    { name: "MTTD", full: "Mean Time to Detect", desc: "Avg time from attack start to detection" },
    { name: "MTTR", full: "Mean Time to Respond", desc: "Avg time from detection to resolution" },
    { name: "MTTA", full: "Mean Time to Acknowledge", desc: "How quickly analysts begin working alert" },
    { name: "Dwell Time", full: "Attacker Presence Duration", desc: "How long attacker remains undetected" },
  ];
  metrics.forEach((m, i) => {
    const y = 0.67 + i * 1.12;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y, w: 4.25, h: 1.0, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
    s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y, w: 4.25, h: 0.06, fill: { color: C.teal } });
    s.addText(m.name, { x: 5.52, y: y + 0.1, w: 2.5, h: 0.28, fontFace: FONT_HEAD, fontSize: 12, bold: true, color: C.teal, margin: 0 });
    s.addText(m.full, { x: 5.52, y: y + 0.4, w: 3.9, h: 0.22, fontFace: FONT_BODY, fontSize: 9.5, bold: true, color: C.light, margin: 0 });
    s.addText(m.desc, { x: 5.52, y: y + 0.64, w: 3.9, h: 0.28, fontFace: FONT_BODY, fontSize: 9, color: C.muted, margin: 0 });
  });
});

// Alert Triage Steps
contentSlide("7-Step Alert Triage Process", s => {
  const steps = [
    { n: "1", title: "READ THE ALERT", desc: "Understand what rule triggered and the underlying data." },
    { n: "2", title: "ENRICH CONTEXT", desc: "Look up source/dest IP, user account, hostname in asset inventory and threat intel." },
    { n: "3", title: "REVIEW RELATED EVENTS", desc: "Query SIEM for other events from same source in past 24–72 hours." },
    { n: "4", title: "PIVOT ON IoCs", desc: "If a malicious IP or hash appears, search for it across all systems." },
    { n: "5", title: "DETERMINE LEGITIMACY", desc: "Known tool? Authorized activity? Scheduled task? False positive?" },
    { n: "6", title: "CLASSIFY & DOCUMENT", desc: "Record findings in ticketing system (ServiceNow, JIRA)." },
    { n: "7", title: "ESCALATE OR CLOSE", desc: "Escalate true positives; close false positives with clear reasoning." },
  ];
  steps.forEach((step, i) => {
    const col = i < 4 ? 0 : 1;
    const row = col === 0 ? i : i - 4;
    const x = 0.35 + col * 4.85;
    const y = 0.67 + row * 1.2;
    s.addShape(pres.shapes.OVAL, { x, y: y + 0.1, w: 0.55, h: 0.55, fill: { color: C.teal } });
    s.addText(step.n, { x, y: y + 0.1, w: 0.55, h: 0.55, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: C.dark, align: "center", valign: "middle", margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.65, y, w: 4.05, h: 1.05, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
    s.addText(step.title, { x: x + 0.78, y: y + 0.06, w: 3.8, h: 0.28, fontFace: FONT_HEAD, fontSize: 10, bold: true, color: C.teal, margin: 0 });
    s.addText(step.desc, { x: x + 0.78, y: y + 0.38, w: 3.8, h: 0.58, fontFace: FONT_BODY, fontSize: 9.5, color: C.light, margin: 0 });
  });
});

// ── SECTION 5: Incident Response ──
sectionHeader(5, "Incident Response", "NIST SP 800-61 lifecycle, containment & forensics");

tableSlide("IR Lifecycle — NIST SP 800-61",
  ["Phase", "Description", "Key Actions"],
  [
    ["1. Preparation", "Build IR capability before an incident occurs.", "IR plan, CSIRT assembly, monitoring tools, tabletop exercises"],
    ["2. Detection & Analysis", "Identify incidents via alerts, reports, or threat hunting.", "Analyze evidence to determine scope and severity"],
    ["3. Containment", "Isolate affected systems. Short-term and long-term strategies.", "Network isolation, host quarantine, account disablement"],
    ["4. Eradication", "Remove root cause of the incident.", "Delete malware, close attack vectors, patch, reset credentials"],
    ["5. Recovery", "Restore systems, validate integrity, monitor closely.", "Restore from clean backups, verify before returning to prod"],
    ["6. Post-Incident", "Document, improve, prevent recurrence.", "Lessons learned, incident report, security control updates"],
  ],
  [2.2, 3.5, 3.6]
);

contentSlide("Containment Strategies & Forensic Evidence", s => {
  const contain = [
    "Network Isolation — VLAN quarantine at firewall/switch level",
    "Host Isolation — EDR remote endpoint isolation from network",
    "Account Disablement — disable compromised AD/IAM accounts",
    "IP/Domain Blocking — add IoCs to firewall & DNS sinkholes",
    "Traffic Redirection — sinkhole C2 traffic for intelligence",
    "Credential Reset — force-reset all potentially affected accounts",
  ];
  card(s, 0.35, 0.67, 4.7, 4.65, "CONTAINMENT STRATEGIES", C.blueDim, contain);

  // Severity
  const sev = [
    { p: "P1 CRITICAL", color: C.red, desc: "Active breach, data exfiltration, ransomware. All-hands response." },
    { p: "P2 HIGH", color: "#E67E22", desc: "Confirmed high-value asset compromise. Response within hours." },
    { p: "P3 MEDIUM", color: C.accent, desc: "Suspicious activity. Investigation within 24 hours." },
    { p: "P4 LOW", color: C.green, desc: "Minor policy violations, informational events." },
  ];
  sev.forEach((sv, i) => {
    const y = 0.67 + i * 1.15;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.3, y, w: 4.35, h: 1.05, fill: { color: C.card }, line: { color: sv.color, width: 2 } });
    s.addText(sv.p, { x: 5.42, y: y + 0.08, w: 4.1, h: 0.3, fontFace: FONT_HEAD, fontSize: 11, bold: true, color: sv.color, margin: 0 });
    s.addText(sv.desc, { x: 5.42, y: y + 0.44, w: 4.1, h: 0.5, fontFace: FONT_BODY, fontSize: 9.5, color: C.light, margin: 0 });
  });
  s.addText("SEVERITY CLASSIFICATION", { x: 5.3, y: 0.67, w: 4.35, h: 0, fontFace: FONT_HEAD, fontSize: 0, color: C.white, margin: 0 });
});

// ── SECTION 6: CTI ──
sectionHeader(6, "Cyber Threat Intelligence", "Types, intelligence cycle, sources & sharing");

tableSlide("CTI Types & Sharing Standards",
  ["Type", "Level", "Description & Use Case"],
  [
    ["Strategic", "Executive", "High-level, non-technical. Trend reports. Informs risk investment & policy."],
    ["Operational", "Management", "Context about specific attacks or actor profiles. Security management decisions."],
    ["Tactical", "Architect", "Adversary TTPs — how threat actors operate. Used to design security controls."],
    ["Technical", "SOC/SIEM", "Specific IoCs (IPs, hashes, domains). Most perishable — changes within hours/days."],
    ["STIX 2.1", "Standard", "Structured language for describing CTI objects, campaigns, indicators, actors."],
    ["TAXII", "Protocol", "Trusted sharing of STIX intelligence over HTTPS between organizations."],
    ["TLP", "Classification", "RED = restricted; AMBER = limited; GREEN = community; WHITE = public."],
  ],
  [1.8, 1.8, 5.7]
);

contentSlide("Pyramid of Pain & Intelligence Cycle", s => {
  // Pyramid of Pain
  const levels = [
    { label: "TTPs", desc: "Tactics, Techniques & Procedures", color: C.red, w: 4.5, pain: "HARDEST TO CHANGE" },
    { label: "Tools", desc: "Software & utilities used by attacker", color: "#E67E22", w: 3.8, pain: "" },
    { label: "Network/Host Artifacts", desc: "Registry keys, specific filenames, URIs", color: C.accent, w: 3.1, pain: "" },
    { label: "Domain Names", desc: "Attacker's C2 domains", color: "#27AE60", w: 2.4, pain: "" },
    { label: "IP Addresses", desc: "Source IPs used by attacker", color: C.blue, w: 1.7, pain: "" },
    { label: "Hash Values", desc: "File MD5/SHA256 checksums", color: C.muted, w: 1.0, pain: "TRIVIAL TO CHANGE" },
  ];
  s.addText("PYRAMID OF PAIN", { x: 0.35, y: 0.67, w: 5.0, h: 0.3, fontFace: FONT_HEAD, fontSize: 11, bold: true, color: C.teal, margin: 0 });
  levels.forEach((l, i) => {
    const y = 5.25 - i * 0.73;
    const x = 0.35 + (4.5 - l.w) / 2;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: l.w, h: 0.62, fill: { color: l.color + "55" }, line: { color: l.color, width: 1 } });
    s.addText(l.label, { x, y: y + 0.04, w: l.w, h: 0.26, fontFace: FONT_HEAD, fontSize: 8.5, bold: true, color: l.color, align: "center", margin: 0 });
    s.addText(l.desc, { x, y: y + 0.32, w: l.w, h: 0.22, fontFace: FONT_BODY, fontSize: 7, color: C.light, align: "center", margin: 0 });
  });

  // Intelligence Cycle
  const cycle = ["Planning & Direction", "Collection", "Processing", "Analysis", "Dissemination", "Feedback"];
  s.addText("INTELLIGENCE CYCLE", { x: 5.5, y: 0.67, w: 4.0, h: 0.3, fontFace: FONT_HEAD, fontSize: 11, bold: true, color: C.teal, margin: 0 });
  cycle.forEach((c, i) => {
    const y = 1.05 + i * 0.75;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.5, y, w: 4.15, h: 0.62, fill: { color: C.card }, line: { color: i % 2 === 0 ? C.blue : C.teal, width: 1 } });
    s.addText(`${i + 1}`, { x: 5.5, y, w: 0.45, h: 0.62, fontFace: FONT_HEAD, fontSize: 16, bold: true, color: i % 2 === 0 ? C.blue : C.teal, align: "center", valign: "middle", margin: 0 });
    s.addText(c, { x: 6.0, y: y + 0.15, w: 3.55, h: 0.3, fontFace: FONT_BODY, fontSize: 11, color: C.light, valign: "middle", margin: 0 });
  });
});

// ── SECTION 7: Log Analysis ──
sectionHeader(7, "How to Analyze a Log", "Methodology, patterns, tools & queries");

contentSlide("7-Step Log Analysis Methodology", s => {
  const steps = [
    { n: "1", t: "COLLECT", d: "Gather all relevant logs via SIEM query or export from all relevant sources." },
    { n: "2", t: "NORMALIZE", d: "Parse into consistent fields: timestamp, source IP, dest IP, user, action, result." },
    { n: "3", t: "FILTER", d: "Remove known-good baseline noise. Focus on relevant time range and systems." },
    { n: "4", t: "SORT & TIMELINE", d: "Order events chronologically to understand the sequence of actions." },
    { n: "5", t: "CORRELATE", d: "Connect events across multiple log sources. Link firewall deny with EDR process event." },
    { n: "6", t: "ENRICH", d: "Geolocate IPs, VirusTotal hash lookups, check domains in threat intel, identify asset owner." },
    { n: "7", t: "INTERPRET", d: "Apply analyst judgment. Does this match known attack techniques? Document findings." },
  ];
  steps.forEach((st, i) => {
    const col = i < 4 ? 0 : 1;
    const row = col === 0 ? i : i - 4;
    const x = 0.35 + col * 4.85;
    const y = 0.67 + row * 1.2;
    const clr = [C.teal, C.blue, C.accent, C.green, "#9B59B6", "#E74C3C", C.tealDim][i];
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.5, h: 1.05, fill: { color: C.card }, line: { color: clr, width: 1 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.45, h: 1.05, fill: { color: clr } });
    s.addText(st.n, { x, y, w: 0.45, h: 1.05, fontFace: FONT_HEAD, fontSize: 18, bold: true, color: C.dark, align: "center", valign: "middle", margin: 0 });
    s.addText(st.t, { x: x + 0.55, y: y + 0.08, w: 3.8, h: 0.28, fontFace: FONT_HEAD, fontSize: 10, bold: true, color: clr, margin: 0 });
    s.addText(st.d, { x: x + 0.55, y: y + 0.4, w: 3.8, h: 0.56, fontFace: FONT_BODY, fontSize: 9, color: C.light, margin: 0 });
  });
});

// Attack Patterns
contentSlide("Common Attack Patterns in Logs", s => {
  const patterns = [
    { title: "BRUTE FORCE / CREDENTIAL STUFFING", color: C.red, items: [
      "Many EventID 4625 (failed logon) from same source in short time",
      "Multiple usernames attempted from one IP address",
      "Success after many failures = confirmed account compromise",
    ]},
    { title: "PORT SCANNING", color: "#E67E22", items: [
      "One source IP connecting to many hosts on same port",
      "Or one IP connecting to many ports on a single host",
      "Firewall DENY logs showing pattern across sequential ports",
    ]},
    { title: "MALWARE C2 BEACONING", color: C.accent, items: [
      "Regular, periodic DNS queries to same domain (e.g. every 60s)",
      "Consistent small HTTP POST requests at regular intervals",
      "DNS queries to DGA-generated or newly registered domains",
    ]},
    { title: "LATERAL MOVEMENT", color: C.teal, items: [
      "SMB (port 445) connections between workstations",
      "Admin share access (\\\\host\\C$, \\\\host\\admin$)",
      "Pass the Hash: Logon Type 3 / NTLM from many hosts",
    ]},
    { title: "DATA EXFILTRATION", color: C.blue, items: [
      "Large outbound transfers to external/unknown IPs",
      "HTTPS traffic to newly registered or rare domains",
      "DNS TXT queries with unusually long subdomains (tunneling)",
    ]},
    { title: "LOG TAMPERING", color: "#9B59B6", items: [
      "EventID 1102 — Security audit log cleared",
      "EventID 104 — System log cleared",
      "Gaps in timestamps or sudden reduction in log volume",
    ]},
  ];
  patterns.forEach((p, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    card(s, 0.35 + col * 3.15, 0.67 + row * 2.35, 3.0, 2.2, p.title, p.color, p.items);
  });
});

// SIEM Query Slide
contentSlide("Key Log Fields & Sample SIEM Query", s => {
  // Key fields table
  const fields = [
    ["Timestamp", "Validate timezone. Gaps may indicate log tampering."],
    ["Source IP", "Internal vs external? Known bad? Geo match expected?"],
    ["Dest IP/Port", "Unusual ports indicate scanning or C2 communication."],
    ["User Account", "Is this account expected to do this action?"],
    ["Action/Event", "Login, file access, process execution, network connection."],
    ["Result/Status", "Repeated failures → success = brute force confirmed."],
    ["User Agent", "Python-requests or empty UA = scripted/automated request."],
    ["Bytes Transferred", "Large outbound volumes may indicate exfiltration."],
    ["Process/Command", "Processes from temp dirs or encoded PowerShell = red flag."],
  ];

  s.addShape(pres.shapes.RECTANGLE, { x: 0.35, y: 0.67, w: 5.6, h: 4.65, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
  s.addText("KEY LOG FIELDS TO ANALYZE", { x: 0.47, y: 0.72, w: 5.3, h: 0.28, fontFace: FONT_HEAD, fontSize: 10, bold: true, color: C.teal, margin: 0 });
  fields.forEach((f, i) => {
    const y = 1.1 + i * 0.47;
    s.addText(f[0], { x: 0.47, y, w: 1.7, h: 0.38, fontFace: FONT_HEAD, fontSize: 9, bold: true, color: C.blue, margin: 0 });
    s.addText(f[1], { x: 2.2, y, w: 3.6, h: 0.38, fontFace: FONT_BODY, fontSize: 9, color: C.light, margin: 0 });
  });

  // Splunk query
  s.addShape(pres.shapes.RECTANGLE, { x: 6.15, y: 0.67, w: 3.5, h: 4.65, fill: { color: C.darker }, line: { color: C.teal, width: 1 } });
  s.addText("SPLUNK — BRUTE FORCE DETECTION", { x: 6.27, y: 0.72, w: 3.2, h: 0.28, fontFace: FONT_HEAD, fontSize: 8.5, bold: true, color: C.teal, margin: 0 });
  const query = "index=windows\nEventCode=4625\n| stats count by\n  src_ip, Account_Name\n| where count > 10\n| sort - count";
  s.addText(query, { x: 6.27, y: 1.12, w: 3.25, h: 1.4, fontFace: "Consolas", fontSize: 9.5, color: C.green, margin: 0 });
  s.addText("This query counts failed logon events (4625) per source IP and username. Threshold of 10+ attempts flags likely brute force activity. Tune the threshold to your organization's baseline.", {
    x: 6.27, y: 2.65, w: 3.25, h: 1.5, fontFace: FONT_BODY, fontSize: 9, color: C.muted, margin: 0
  });
  const tools2 = ["Splunk (SPL)", "Elastic/ELK (KQL)", "Microsoft Sentinel", "grep / awk / sed", "jq (JSON logs)", "Zeek / Wireshark", "Sigma (portable rules)"];
  s.addText("LOG ANALYSIS TOOLS", { x: 6.27, y: 4.22, w: 3.2, h: 0.24, fontFace: FONT_HEAD, fontSize: 8.5, bold: true, color: C.accent, margin: 0 });
  const tItems = tools2.map((t, i) => ({ text: t, options: { bullet: true, color: i % 2 === 0 ? C.light : C.muted, fontSize: 8.5, fontFace: FONT_BODY, breakLine: i < tools2.length - 1 } }));
  s.addText(tItems, { x: 6.27, y: 4.5, w: 3.25, h: 0.75, valign: "top", margin: 0 });
});

// ── SECTION 8: Quick Reference ──
sectionHeader(8, "Quick Reference", "Acronyms, Event IDs, ATT&CK tactics & IR checklist");

// MITRE ATT&CK
tableSlide("MITRE ATT&CK Tactics",
  ["Tactic", "ID", "Description"],
  [
    ["Initial Access", "TA0001", "How attacker gets in: phishing, exploit, valid accounts, supply chain"],
    ["Execution", "TA0002", "Running malicious code: PowerShell, WMI, scheduled tasks, scripts"],
    ["Persistence", "TA0003", "Maintaining access: registry run keys, services, backdoors"],
    ["Privilege Escalation", "TA0004", "Gaining higher permissions: token manipulation, misconfigurations"],
    ["Defense Evasion", "TA0005", "Avoiding detection: obfuscation, log deletion, LOLBins"],
    ["Credential Access", "TA0006", "Stealing credentials: Mimikatz, LSASS dump, password spraying"],
    ["Lateral Movement", "TA0008", "Moving through network: PsExec, WMI, Pass the Hash, RDP"],
    ["Command & Control", "TA0011", "Communicating with compromised systems: beaconing, DNS tunneling"],
    ["Exfiltration", "TA0010", "Stealing data: cloud upload, DNS tunneling, encrypted channels"],
    ["Impact", "TA0040", "Final objectives: ransomware, data destruction, wiper malware"],
  ],
  [2.5, 1.2, 5.6]
);

// IR Checklist + Acronyms
contentSlide("IR Checklist & Key Acronyms", s => {
  const checklist = [
    "Alert received — triage and classify severity",
    "Notify IR team per severity matrix",
    "Preserve evidence — memory and disk images BEFORE touching system",
    "Contain — isolate affected systems from network",
    "Investigate — correlate logs, identify attack vector and scope",
    "Map to MITRE ATT&CK — document all TTPs observed",
    "Block IoCs — add malicious indicators to blocklists",
    "Notify stakeholders — follow communication plan",
    "Eradicate — remove malware, patch, reset credentials",
    "Recover — restore from clean backup, verify integrity",
    "Monitor — heightened monitoring post-incident for 30 days",
    "Post-incident report — timeline, root cause, lessons learned",
  ];
  card(s, 0.35, 0.67, 4.7, 4.65, "INCIDENT RESPONSE CHECKLIST", C.tealDim, checklist);

  // Acronyms
  const acronyms = [
    ["SOC", "Security Operations Center"],
    ["SIEM", "Security Info & Event Management"],
    ["EDR", "Endpoint Detection & Response"],
    ["SOAR", "Security Orchestration, Automation & Response"],
    ["CTI", "Cyber Threat Intelligence"],
    ["TTP", "Tactics, Techniques & Procedures"],
    ["IoC", "Indicator of Compromise"],
    ["APT", "Advanced Persistent Threat"],
    ["LOLBin", "Living Off the Land Binary"],
    ["MTTD/MTTR", "Mean Time to Detect / Respond"],
    ["DGA", "Domain Generation Algorithm"],
    ["C2 / C&C", "Command and Control server"],
  ];
  acronyms.forEach((a, i) => {
    const col = i < 6 ? 0 : 1;
    const row = col === 0 ? i : i - 6;
    const x = 5.3 + col * 2.25;
    const y = 0.67 + row * 0.75;
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.1, h: 0.65, fill: { color: C.card }, line: { color: C.cardBdr, width: 1 } });
    s.addText(a[0], { x: x + 0.08, y: y + 0.04, w: 1.95, h: 0.25, fontFace: FONT_HEAD, fontSize: 9.5, bold: true, color: C.teal, margin: 0 });
    s.addText(a[1], { x: x + 0.08, y: y + 0.34, w: 1.95, h: 0.24, fontFace: FONT_BODY, fontSize: 8, color: C.muted, margin: 0 });
  });
});

// ── Final slide ──
const final = pres.addSlide();
final.background = { color: C.darker };
final.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.3, w: 10, h: 1.0, fill: { color: C.navy } });
final.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.3, w: 10, h: 0.06, fill: { color: C.teal } });
final.addShape(pres.shapes.RECTANGLE, { x: 0, y: 3.24, w: 10, h: 0.06, fill: { color: C.teal } });
final.addText("STAY VIGILANT.", { x: 0.5, y: 2.38, w: 9, h: 0.55, fontFace: FONT_HEAD, fontSize: 32, bold: true, color: C.teal, align: "center", margin: 0 });
final.addText("DETECT EARLY.  RESPOND DECISIVELY.", { x: 0.5, y: 2.82, w: 9, h: 0.45, fontFace: FONT_HEAD, fontSize: 20, bold: true, color: C.white, align: "center", margin: 0 });
final.addText("Blue Teaming & SOC Operations — 2025", { x: 0.5, y: 4.8, w: 9, h: 0.35, fontFace: FONT_BODY, fontSize: 11, color: C.muted, align: "center", margin: 0 });

pres.writeFile({ fileName: "BlueTeaming_SOC_Operations.pptx" })
  .then(() => console.log("Done!"))
  .catch(e => { console.error(e); process.exit(1); });
