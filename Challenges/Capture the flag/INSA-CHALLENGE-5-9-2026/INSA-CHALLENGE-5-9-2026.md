**Target** : https://100.55.41.187/

---
#### Plan
- **Enumeration**
	- Nmap scan for open services
	- subdomain search through `subfind3r`
- **Vulnerability detection**
	- SQL injection
	- XSS
---

# Execution

## Enumeration
### **NMAP** results
![[INSA-CHALLENGE-9-5-2026-NMAP_Results.png]]
NMAP scan results show that port **80** and **8080** are open (*HTTP*, and likely *SMTP*). Both running on *`Node.js`* + *`Express`*.

**Note** : We can safely assume port **20**(*SSH*) is hardened as the IP is hosted by **AWS**.

