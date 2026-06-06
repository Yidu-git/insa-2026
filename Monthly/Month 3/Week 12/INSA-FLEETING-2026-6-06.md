---
cssclasses:
  - jbm-note
---
- **REVISION**
	1. Mobile security
	2. RCE
	3. Windows Vuln testing
	4. Lateral Movement
	5. Privilege escalation
	6. Post exploitation
 - **Research Topics**
	1. Lateral Movement
	2. Privilege escalation in Linux
	3. Post exploitation
		1. Local enumeration
		2. Process enumeration
		3. User enumeration
			- Checking the existence of other users
		4. Host enumeration
		5. Credential enumeration
			- Checking `.env` files
			- Checking databases or opening databases internally
			- Checking hardcoded information
			- Checking backups
		6. File enumeration
			- Checking filesystem
			- Checking common vulnerabilities
		7. Automation
			- Benefits and limitation
		8. Protocol
	4. Commands used in enumeration
	5. Report writing

**To check**
- `linpeas.sh`
- `sudo -l`
- `find / -perm -4000 2> /dev/null`
- `HackTricks`
- `NVD CVSS calculator`
- `...`

# Lateral Movement
---
...

# Privilege escalation
---
## Enumeration
To gain higher access in a system, the first step is always to find out the common paths to that access. One of these common paths or steps is writing root executable files or files that are run as **root**. These files are important to escalating user privilege.

## `linpeas`


# Post exploitation
---
Post exploitation is the process of sustaining persistence after the initial attack. With out the post exploitation process, the attacker loses access after closing a session or reboot and will have to restart the process they went through to get access in the first place.

## Risk assessment
Before trying to gain persistence, an attacker must assess the risks involved with going through with a plan. For example: if an attacker gains root access, the attacker can't create a new user to regain access. The attacker must hide their process of gaining access.

## Rules of engagement and scope considerations
After enumerating a system and gaining access to it, the attacker must be careful about how to engage. They must scope out their next potential attack.

# Report writing
---
## What is report writing?
**Report writing** is a fundamental part of working in teams in any scenario. It takes skill and reflection to write a report. Report writing is especially common cyber security, particularly in incident response, vulnerability intelligence and pen testing.

## Types of report writing
## Do's
- Proof of concept
- Impact
- CVSS calculation
- Reproducibility
- Documentation
	- How
	- When
- Suggestions/Recommendations
- Summary
- Priority

