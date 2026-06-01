---
cssclasses:
  - jbm-note
  - underline-headers
Date: 2026-05-31
---

# Mobile security Challenge

| **Target** :LiTarget:              | *Mobile application* |
| ---------------------------------- | -------------------- |
| Date :LiCalendar:                  | 31/5/2026            |
| Main attack type                   | ...                  |
| Secondary attack type              | ...                  |
| Tools :LiToolCase: :               | JADX, GenY Motion    |
| Criticality :RiAlarmWarningLine: : | **...**              |

---
# **RESULTS**
---
## Flags found
1. First flag
	- *F1ag_0n3*
2. Second flag
	- *...*
3. Third flag
	- *...*
4. Fourth flag
	- *...*
5. Fifth flag
	- *...*
6. Sixth flag
	- *...*
7. Seventh flag
	- *...*
8. Eighth flag
	- *...*
9. ... flag
	- *...*
10. ... flag
	- *...*
11. ... flag
	- *...*
12. ... flag
	- *...*


---
# Preparation
---
## Tools
1. **JADX**
	- On :SiKalilinux: *Kali Linux*
2. **Android studio AVD** (ROOTED)
	- Android 11 (API 30)

---
# Initial investigation/enumeration
---
## **Enumeration**
### Looking through the app
The app is a simple CTF with 18 flags, it includes a flag overview and and `XSSTEXT` section that reflects text inserted into the input field. This section is not used to find other flags, as stated by the text : `Fun no flag vulnerable XSS field to test payloads.`

## **Vulnerability scanning**
...

---
# Exploiting and  Investigation
---
## First flag
The *`FLAG ONE - LOGIN`* section contains a single input field, this can likely be exploited through checking the source code.

Checking the source code with JADX-GUI reveals the first flag as a string. It is located in `First_Flag_Activity`. Inserting the flag into the input field on the app confirms the flag.

## Second flag
The *`FLAG TWO - EXPORTED ACTIVITY`* section contains the text : 
*There is a way to bypass the main activity and invoke other activities that are exported.*.

This hints at a vulnerability that can be exploited through **`adb`**. Checking the source code