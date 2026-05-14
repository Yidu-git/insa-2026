# Foxy proxy
A chromium extension that allows the use of proxies to connect to a site.
# Vertical vs Horizontal
## What is access control?

Access control is the application of constraints on who or what is authorized to perform actions or access resources. In the context of web applications, access control is dependent on authentication and session management:

- **Authentication** confirms that the user is who they say they are.
- **Session management** identifies which subsequent HTTP requests are being made by that same user.
- **Access control** determines whether the user is allowed to carry out the action that they are attempting to perform.

Broken access controls are common and often present a critical security vulnerability. Design and management of access controls is a complex and dynamic problem that applies business, organizational, and legal constraints to a technical implementation. Access control design decisions have to be made by humans so the potential for errors is high.
### Vertical access controls

**Vertical access controls** are mechanisms that restrict access to sensitive functionality to *specific types of users*.

With vertical access controls, different types of users have access to different application functions. For example, an administrator might be able to modify or delete any user's account, while an ordinary user has no access to these actions. Vertical access controls can be more fine-grained implementations of security models designed to enforce business policies such as separation of duties and least privilege.

### Horizontal access controls

**Horizontal access controls** are mechanisms that restrict access to resources to *specific users*.

With horizontal access controls, different users have access to a subset of resources of the same type. For example, a banking application will allow a user to view transactions and make payments from their own accounts, but not the accounts of any other user.

# IDOR (Insecure Direct Object Reference)
==Insecure Direct Object Reference== (IDOR) is a broken access control vulnerability where an application uses user-supplied input to directly access an object (e.g., database key, file) without validating if the user is authorized. Attackers exploit this by modifying parameters, such as changing `?id=123` to `?id=124`, to access, modify, or delete sensitive data of other users.

# `seclist`
A Library of powerful word lists that go beyond the common **`rockyou.txt`** found on every **kali** machine.

# Web security
## Attack surface
**Attack surface** in the field of cyber security is the collection of target interactions in a system. To increase the attack surface of a system we use reconnaissance.
## Recon Enum and Analysis
### Reconnaissance
Discovery and gathering information about targets using public information. Recon can be done with tools like *`nmap`* or search engines like *google*.
### Enumeration
Is a structured expansion of an attack surface by converting raw data into actionable intelligence by organizing and categorizing findings.
### Analysis
After gathering resources, We can map the attack surface to find exploits and find targets.
## Active vs Passive recon
### Passive recon
- Public info
- No direct interaction
- Slower
- Low risk
- Examples : WHOIS, DS records search engines
### Active recon
- Direct interaction
- Higher visibility (logs, sessions)
- Examples : port scanning (`nmap`), direct brute forcing (`hashcat`)
## Basics
- Domains and subdomains
- APIs
- Backup paths
- Admin panels
- robots.txt
- Directories and files
## Go buster
Fast directory enumeration
```Shell
gobuster dir -u URL -w <WORDLIST> [options]
```
### Extensions
```Shell
gobuster dir -u http://lab.example.local \ -w common.txt -x php,txt,html
```

### Threads (Multi threading)
```shell
gobuster dir -u http://lab.example.local -w common.txt -t 20
```

## Recon tips
#### Example case : Enterprise
- Collect information on each employee (example through LinkedIn or google)
- Check social data like pictures and discussions
