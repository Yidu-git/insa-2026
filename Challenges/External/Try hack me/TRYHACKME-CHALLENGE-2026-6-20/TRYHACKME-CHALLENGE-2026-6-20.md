---
cssclasses:
  - jbm-note
Date: 2026-06-20
tags:
  - THMChallenge
---
# **RDP** Challenge

| **Target** :LiTarget:            | *Try hack me machine(room:stuxctf)*              |
| -------------------------------- | ------------------------------------------------ |
| Date :LiCalendar:                | 20/06/2026                                       |
| Main attack type                 | RDP                                              |
| Secondary attack type            | Privilege escalation                             |
| Tools :LiToolCase:               | NMAP, Python, `xfreerdp`, GOBUSTER               |
| Criticality :RiAlarmWarningLine: | **9**, **Critical** - RDP & Privilege escalation |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. User.txt?
	- *3b99fbdc6d430bfb51c72c651a261927*
2. Root.txt?
	- *7958b569565d7bd88d10c6f22d1c4063*
3. Hidden directory
	- */retro*
---
# Preparation
---
## Resources
- Resources / Information provided in-room
- [CVE-2017-0213](https://github.com/SecWiki/windows-kernel-exploits/blob/master/CVE-2017-0213/CVE-2017-0213_x64.zip) - Windows exploit
- RDP Software : `xfreerdp`

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
#### Simple scan
```bash
sudo nmap -Pn -sS -sV TARGET
```
```
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
3389/tcp open  ms-wbt-server Microsoft Terminal Services
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
retro                (Status: 301) [Size: 151] [--> http://10.130.152.208/retro/]
```

## **Vulnerability scanning**
### ...

---
# Exploiting and Investigation
---
## Enumerating the server
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-20/Images/TARGET_PAGE_HOME.png]]
The **HTTP** server on port 80 shows a default Microsoft Windows Server page. Trying to find secret endpoints with `gobuster` and the *`directory-list-2.3-medium.txt`* wordlists shows a working endpoint:**`retro`**.

![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-20/Images/TARGET_PAGE_BLOG_WITH_PASSWORD.png]]
Looking further into the site, seems to be a blog service. Looking for any information posted early in the sites history reveals the password of a user "Wade".

## Gaining access to the server
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-20/Images/TARGET_RDP_ACCESS.png]]

Since port **3389** was open, it was safe to assume this was the password to the RDP service. Using the `xfreerdp` command provides a clean way to access the server.
```bash
xfreerdp /u:wade /v:TARGET
```
The user flag was located under a *`user.txt`* file.

## Privilege escalation
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-20/Images/TARGET_RDP_ROOT_ACCESS.png]]To get the root flag, we need to get some way of exploiting the old windows system by downloading a payload (**CVE-2017-0213**). By running a temporary python server, the payload was transferred to the machine giving us access to the `Administrator` user. The root flag was located under a *`root.txt`* file in the admins desktop.