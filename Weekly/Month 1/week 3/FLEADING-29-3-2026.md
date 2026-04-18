**Encapsulation** is adding or attaching headers to a main data packet (ex: HTTP header, TCP/UCP header, IP header, MAC header, etc...). This process is used to make sure that the right data arrives to the right location/user.

# Attacks
### Physical layer
- Destruction
- Wire tapping
- JAMMING
### Datalink layer
- ARP poisoning
- MAC spoofing/Spoofing
### Network layer
- DoS / DDoS
- MITM

### Transport Layer
- SYN packing

### Session Layer
- Session hijacking

### Presentation Layer
- MITM
- Encryption attack

### Application layer
- SQL injection
- DNS poisoning

---
# Wireshark
**Wireshark** is a packet capture service. It captures packets going to your device, but it can also be used to capture packets going to another device by routing their network through your device (MIMT).

---

[Internet Control Message Protocol (ICMP)](https://www.cloudflare.com/learning/ddos/glossary/internet-control-message-protocol-icmp/) is a network layer protocol used primarily by routers and hosts to **communicate network health, diagnose connection issues, and report errors**, such as when a requested service is unavailable or a packet is too large. It is essential for network diagnostics tools like `ping` and `traceroute`, helping identify latency and routing paths.

---

**DNS** (*Domain name service*) is a service that returns the IP of a site/server upon receiving a URL / Domain.

---

# IPv6

As compared to IPv4, IPv6 has 16 octets (bytes) which is 4x the amount of octets in an IPv4 address. This allows for a far greater amount of possible combinations.

IPv6 is split up into groups of 2 octets separated by a colon `:`. And leading 0s are represented with double colons `::`.

---

# Ping command (`ping google.com`)
The **`ping`** command is a command used to test if a computers network is working or if a service is running. If both of those cases are true, it returns the IP and the size of data returned.
Example
```Bash
ping google.com
```
Returns:
```
Pinging google.com [172.217.169.238] with 32 bytes of data
```

# Netstat command (`netstat`)
The **`netstat`** command is used to check the status of network while returning active connections.

---

`C:\Windows\System32\winevt\Logs`
# Windows event viewer
WEV is an **SIEM** (Security Information and Event Management) that helps software engineers test software.


---

A **PowerShell downgrade attack** is a technique used by attackers to bypass modern security controls (like *AMSI*, *Script Block Logging*, or *Constrained Language Mode*) by forcing PowerShell to run an older, less secure version (e.g., PowerShell 2.0). This evasion technique allows malicious scripts to execute without triggering advanced detection mechanisms.

---
