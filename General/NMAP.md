#NMAP #CyberSecurity 
# Topics to cover
- What is NMAP ?
- What is NMAP used for ?
- Which OSI layers does NMAP interact with most ?
- How does TCP scan work ?
- How does UDP scan work ?
- Why are UDP scans slower ?
- What does OS detection try to identify ?
- What is NSE (Nmap Scripting Engine) ?
- Common flags used on a scanning target
- What is the difference between `-sS` and `-sT` ?
- What does a "filtered port" mean ?
- How do ethical hackers use Nmap for firewall evasion ?
- Nmap `xmas` scan

# Intro
This note contains notes on Nmap and its uses. Nmap is a commonly used tool in cybersecurity to discover networks and security auditing.
++

---

tags:

- cybersecurity
- networking
- nmap
- pentesting
- tools aliases:
- Network Mapper
- nmap reference created: 2026-04-04

---

# 🗺️ NMAP — Network Mapper Reference

> [!abstract] Overview Nmap (Network Mapper) is a free, open-source tool for network discovery and security auditing. Originally released in 1997 by Gordon Lyon (Fyodor), it is the industry-standard utility for mapping networks, identifying hosts, discovering open ports, and fingerprinting services.

---

## 1. What is Nmap?

Nmap works by sending crafted packets to target hosts and analysing the responses to determine what is running, what ports are open, and what OS is in use.

It runs on **Linux**, **macOS**, and **Windows**, and is routinely used by network administrators, penetration testers, and security researchers.

---

## 2. What is Nmap Used For?

- **Host discovery** — identifying which devices are alive on a network
- **Port scanning** — determining which TCP/UDP ports are open, closed, or filtered
- **Service & version detection** — identifying what application is listening on each port
- **OS fingerprinting** — guessing the operating system of a remote host
- **Vulnerability detection** — running scripts (NSE) to find known weaknesses
- **Firewall & IDS auditing** — testing how security controls respond to different packet types
- **Network inventory** — documenting and auditing what is running on a network

---

## 3. OSI Layers Nmap Interacts With

Nmap primarily operates at **Layers 3 and 4**, with some activity at Layer 2 for local network discovery.

|Layer|Name|Nmap's Use|
|---|---|---|
|Layer 2|Data Link|ARP ping for local LAN host discovery|
|Layer 3|Network|IP packet crafting, ICMP pings, traceroute|
|Layer 4|Transport|TCP/UDP port scanning, flag manipulation|
|Layer 7|Application|Service version detection, NSE script interactions|

---

## 4. How Does a TCP Scan Work?

Nmap offers two main TCP scanning modes: the **SYN scan** (`-sS`) and the **Connect scan** (`-sT`). Both follow the TCP three-way handshake model, but differ in how much of it they complete.

### The Three-Way Handshake

```
Client  ──── SYN ────►  Server
Client  ◄── SYN/ACK ──  Server
Client  ──── ACK ────►  Server   (connection established)
```

### SYN Scan (`-sS`) — "Half-Open Scan"

- Sends a **SYN** packet to the target port
- **Open port** → target replies with `SYN/ACK` — Nmap immediately sends `RST` to abort
- **Closed port** → target replies with `RST/ACK`
- **Filtered port** → no response, or ICMP unreachable

> [!tip] Why it's stealthy The connection is never fully established, so it typically won't appear in application-level logs.

### Connect Scan (`-sT`) — "Full Connect Scan"

- Completes the full three-way handshake via the OS `connect()` syscall
- More reliable when **raw socket privileges are unavailable** (no root/admin)
- Slower and more visible — every connection is logged by the target application

---

## 5. How Does a UDP Scan Work?

UDP is connectionless — there is no handshake. Nmap performs UDP scanning with the `-sU` flag.

```
Nmap  ──── UDP Packet ────►  Target Port

  Open:        No response  (or application-specific reply)
  Closed:      ICMP Port Unreachable (type 3, code 3)
  Filtered:    ICMP Unreachable (other type/code) or no response
```

- **No response** → port is marked `open|filtered`
- **ICMP Port Unreachable** → port is marked `closed`
- **Application reply** → port is marked `open`

---

## 6. Why Are UDP Scans Slower?

- **No handshake** — Nmap must wait for a timeout before concluding a port is `open|filtered`
- **ICMP rate limiting** — most OSes throttle ICMP Unreachable responses (Linux defaults to ~1/sec), forcing Nmap to slow down
- **Ambiguity** — non-response could mean open or filtered, requiring retransmits to confirm
- **65,535 ports** — without quick `RST` feedback like TCP, full UDP scans can take minutes to hours

> [!tip] Use `--top-ports 100` with `-sU` to scan only the most commonly used UDP ports and save significant time.

---

## 7. What Does OS Detection Try to Identify?

Enabled with **`-O`**, Nmap's OS detection sends TCP, UDP, and ICMP probes and compares responses against a database of **5,000+ known OS fingerprints**.

It attempts to identify:

- **OS family** — Linux, Windows, macOS, FreeBSD, etc.
- **OS version & build** — e.g. Windows 10 1903, Linux kernel 5.x
- **Device type** — router, switch, firewall, printer, phone, general-purpose
- **CPU architecture** — x86, x86-64, ARM, etc.

Fingerprinting analyses subtle TCP/IP stack differences, including:

- Initial **TTL values** in IP headers
- **TCP window sizes** in SYN/ACK responses
- Handling of unusual flag combinations (e.g. FIN sent to an open port)
- **IP ID field sequencing** and ICMP response characteristics

> [!warning] OS detection requires at least **one open and one closed port** to work reliably. Results are given as a probability — never treat them as absolute.

---

## 8. What is the Nmap Scripting Engine (NSE)?

The **Nmap Scripting Engine (NSE)** allows users to write and run **Lua scripts** that automate a wide variety of network tasks. Scripts are invoked with the `--script` flag.

### Script Categories

|Category|Purpose|
|---|---|
|`auth`|Testing authentication credentials and mechanisms|
|`brute`|Brute-force credential attacks against services|
|`discovery`|Gathering additional network information|
|`exploit`|Actively exploiting vulnerabilities|
|`safe`|Non-intrusive scripts safe to run on any target|
|`vuln`|Checking for known CVEs and weaknesses|
|`malware`|Detecting signs of malware or backdoors|

### Usage Examples

```bash
# Run all default safe scripts
nmap -sC target

# Run a specific script
nmap --script=http-title target

# Run all vuln scripts
nmap --script=vuln target

# Run scripts with arguments
nmap --script=http-brute --script-args userdb=users.txt target
```

---

## 9. Common Flags

|Flag|Name|Description|
|---|---|---|
|`-sS`|SYN Scan|Stealthy half-open TCP scan (requires root)|
|`-sT`|Connect Scan|Full TCP connect scan (no root needed)|
|`-sU`|UDP Scan|Scans UDP ports|
|`-sV`|Version Detection|Detects service/version on open ports|
|`-O`|OS Detection|Attempt to identify target OS|
|`-A`|Aggressive|Enables `-sV`, `-O`, `-sC`, and traceroute|
|`-p`|Port Range|Specify ports: `-p 80`, `-p 1-1000`, `-p-` (all)|
|`-T0` to `-T5`|Timing Template|Controls speed: T0=slowest, T5=fastest|
|`-Pn`|No Ping|Skip host discovery, assume host is up|
|`-sC`|Default Scripts|Run default NSE scripts (`--script=default`)|
|`-oN` / `-oX`|Output Format|Save results in normal or XML format|
|`--top-ports N`|Top Ports|Scan the N most commonly used ports|
|`-v` / `-vv`|Verbosity|Increase output verbosity|
|`-n`|No DNS|Skip DNS resolution for faster scans|
|`-iL`|Input List|Read targets from a file|

---

## 10. `-sS` vs `-sT` — What's the Difference?

|Property|`-sS` (SYN / Stealth)|`-sT` (Full Connect)|
|---|---|---|
|Handshake completion|Half-open — RST after SYN/ACK|Full three-way handshake|
|Root required?|Yes (raw sockets)|No (uses OS `connect()`)|
|Speed|Fast|Slower|
|Logged by target?|Usually not (app-level)|Yes — full session opened|
|Stealth|Higher|Lower|
|Default scan?|Yes (if root)|Yes (if no root)|

---

## 11. What Does a "Filtered" Port Mean?

When Nmap reports a port as **filtered**, a packet was sent but no definitive response was received — most commonly because a **firewall, packet filter, or ACL** is silently dropping packets.

```
Port States Nmap Can Report:

  open           — Port is accepting connections
  closed         — Port is reachable, but no service is listening
  filtered       — Packet dropped / no response (firewall likely present)
  open|filtered  — Cannot determine if open or filtered (common with UDP)
  unfiltered     — Port is reachable, but open/closed status is unknown
  closed|filtered — Cannot distinguish closed from filtered
```

> [!note] A `filtered` result does **not** mean the port is necessarily closed — a service may be running behind the firewall. Nmap simply cannot confirm the state.

---

## 12. Firewall Evasion Techniques

> [!warning] Legal Notice All firewall evasion techniques must only be used against systems you have **explicit written authorisation** to test. Unauthorised scanning is illegal in most jurisdictions.

### Fragmentation (`-f`)

Splits packets into small fragments. Some older firewalls fail to reassemble and inspect them correctly.

```bash
nmap -f target
```

### Decoy Scanning (`-D`)

Makes the scan appear to originate from multiple IPs simultaneously, obscuring the real source.

```bash
nmap -D RND:10 target
nmap -D 192.168.1.5,192.168.1.6,ME target
```

### Idle / Zombie Scan (`-sI`)

Uses a third-party "zombie" host with predictable IP ID values — the attacker's IP never touches the target directly.

```bash
nmap -sI zombie_host target
```

### Spoofed Source IP (`-S`)

Sends packets with a forged source IP to test firewall rules. Responses go to the spoofed address, not the attacker.

```bash
nmap -S spoofed_ip -e eth0 target
```

### Custom MTU (`--mtu`)

Manually sets the Maximum Transmission Unit for fine-grained packet fragmentation beyond `-f`.

```bash
nmap --mtu 8 target
```

### Timing & Port Tricks

```bash
# Spoof source port 53 (DNS) — many firewalls allow this through
nmap --source-port 53 target

# Slow scan to avoid rate-based IDS detection
nmap -T1 target   # Sneaky
nmap -T0 target   # Paranoid

# Append random padding to confuse signature-based IDS
nmap --data-length 25 target
```

---

## 13. Xmas Scan (`-sX`)

The **Xmas scan** gets its name because it "lights up" a packet with multiple TCP flags at once — **FIN**, **PSH**, and **URG** — like a Christmas tree full of lights.

```bash
nmap -sX target
# Packet sent with flags: FIN + PSH + URG all set simultaneously
```

### How It Works

Per **RFC 793**, a compliant TCP stack should respond as follows:

```
  No response   →   open | filtered
  RST received  →   closed
  ICMP Unreach  →   filtered
```

### Key Characteristics

- Works **only on RFC 793-compliant** TCP stacks — Windows always sends RST regardless of port state
- Does not complete a connection → does **not appear in application logs**
- Can bypass simple **stateless packet filters** that only block SYN packets
- Less reliable than SYN scans due to OS behaviour differences

### Related Scans

|Scan|Flag|Flags Set|
|---|---|---|
|Xmas Scan|`-sX`|FIN + PSH + URG|
|NULL Scan|`-sN`|None (0 flags)|
|FIN Scan|`-sF`|FIN only|

> [!caution] Xmas scans **will not work correctly against Windows targets**. Use `-sS` or `-sT` for cross-platform TCP scanning.

---

## Quick Reference Cheatsheet

```bash
# Basic host discovery
nmap -sn 192.168.1.0/24

# Quick top-port scan
nmap --top-ports 100 target

# Full aggressive scan
nmap -A -T4 target

# Stealth SYN scan with version + OS detection
sudo nmap -sS -sV -O target

# UDP top ports
sudo nmap -sU --top-ports 100 target

# NSE vulnerability scan
nmap --script=vuln target

# Save output
nmap -oN output.txt -oX output.xml target

# Firewall evasion combo
sudo nmap -sS -f -T1 --source-port 53 -D RND:5 target
```

---

## Related Notes

- [[OSI Model]]
- [[TCP-IP Protocol Suite]]
- [[Firewall & IDS Concepts]]
- [[Penetration Testing Methodology]]
- [[Cybersecurity Certifications Roadmap]]