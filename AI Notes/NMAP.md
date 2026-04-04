# 📡 Nmap Study Notes

## 🔹 What is Nmap?

Nmap (Network Mapper) is an open-source tool used for:

- Network discovery
    
- Port scanning
    
- Service/version detection
    
- OS fingerprinting
    
- Security auditing
    

Created by Gordon Lyon (Fyodor)

---

## 🔹 How Nmap Works

Nmap sends specially crafted packets to targets and analyzes responses.

### Core Techniques:

- TCP SYN scanning (half-open)
    
- TCP connect scanning (full connection)
    
- UDP scanning
    
- ICMP echo (ping)
    

👉 Based on **TCP/IP behavior**

---

## 🔹 Basic Syntax

```
nmap [scan type] [options] [target]
```

### Examples:

```
nmap 192.168.1.1
nmap -p 80,443 example.com
nmap -sS -A 10.0.0.0/24
```

---

## 🔹 Target Specification

- Single IP: `192.168.1.1`
    
- Range: `192.168.1.1-100`
    
- Subnet (CIDR): `192.168.1.0/24`
    
- Domain: `example.com`
    
- File input: `-iL targets.txt`
    

---

## 🔹 Port Scanning

### Common Port States:

- **open** → service is accepting connections
    
- **closed** → reachable but no service
    
- **filtered** → blocked by firewall
    
- **unfiltered** → reachable but unclear
    

### Port Options:

```
-p 80              # single port
-p 1-1000          # range
-p-                # all ports
--top-ports 100    # most common ports
```

---

## 🔹 Scan Types

### 🔸 TCP SYN Scan (Stealth)

```
-sS
```

- Fast and stealthy
    
- Doesn’t complete handshake
    

---

### 🔸 TCP Connect Scan

```
-sT
```

- Full connection
    
- Easier to detect
    

---

### 🔸 UDP Scan

```
-sU
```

- Slower and less reliable
    
- Used for DNS, SNMP, etc.
    

---

### 🔸 Ping Scan (Host Discovery)

```
-sn
```

- Checks if hosts are alive
    

---

## 🔹 Service & Version Detection

```
-sV
```

- Identifies running services and versions
    
- Example output:
    

```
80/tcp open  http Apache 2.4.41
```

---

## 🔹 OS Detection

```
-O
```

- Uses TCP/IP fingerprinting
    
- Compares responses with known OS signatures
    

---

## 🔹 Aggressive Scan

```
-A
```

Enables:

- OS detection
    
- Version detection
    
- Script scanning
    
- Traceroute
    

⚠️ Noisy → easily detected

---

## 🔹 Nmap Scripting Engine (NSE)

Allows automation using scripts.

Docs: [https://nmap.org/book/nse.html](https://nmap.org/book/nse.html)

### Usage:

```
--script <script-name>
```

### Examples:

```
--script vuln
--script http-enum
--script ftp-anon
```

### Script Categories:

- auth (authentication)
    
- vuln (vulnerability detection)
    
- discovery
    
- brute
    
- exploit
    

---

## 🔹 Output Formats

```
-oN output.txt   # normal
-oX output.xml   # XML
-oG output.grep  # grepable
```

---

## 🔹 Timing & Performance

```
-T0 → paranoid (slow)
-T5 → insane (fast)
```

Example:

```
nmap -T4 192.168.1.1
```

---

## 🔹 Firewall Evasion Techniques

- Fragment packets:
    

```
-f
```

- Decoy scan:
    

```
-D RND:10
```

- Spoof source IP:
    

```
-S <IP>
```

- Randomize hosts:
    

```
--randomize-hosts
```

⚠️ Used in advanced pentesting

---

## 🔹 Common Practical Commands

### Quick scan

```
nmap -T4 -F target
```

### Full scan

```
nmap -p- -T4 target
```

### Service detection

```
nmap -sV target
```

### Vulnerability scan

```
nmap --script vuln target
```

---

## 🔹 Use Cases

- Network inventory
    
- Security auditing
    
- Penetration testing
    
- Detecting open ports/services
    
- Finding vulnerabilities
    

---

## 🔹 Legal & Ethical Notes ⚠️

- Only scan systems you **own or have permission to test**
    
- Unauthorized scanning may be illegal
    
- Use lab environments like:
    
    - Metasploitable
        
    - TryHackMe
        
    - Hack The Box
        

---

## 🔹 Learning Progression

1. Basic scans (`-p`, `-sn`)
    
2. Scan types (`-sS`, `-sU`)
    
3. Service detection (`-sV`)
    
4. OS detection (`-O`)
    
5. NSE scripts
    
6. Evasion techniques
    

---

## 🔹 Key Takeaways

- Nmap is essential for networking & cybersecurity
    
- Combines multiple scanning techniques
    
- Highly flexible via scripts
    
- Accuracy depends on network conditions and privileges
    