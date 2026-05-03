# CHALLENGE 01 — Certificate Transparency Enumeration | 100 pts | [ PASSIVE ]
**TARGET** : *bugcroud.com*

TASKS:
1. How many unique subdomains appear across all CT logs for bugcrowd.com 
	 **3685**
2. Which wildcard certificates exist for `*.bugcrowd.com`? List the issuing certificate authorities.
3. Find all subdomains containing the string 'api' or 'dev' — list them in full.
	**15**
### Commands used
Task 1:
```Bash
gobuster dir -u bugcrowd.com -w /usr/share/wordlists/dirb/common.txt
```
Task 2:

Task 3:
```Bash
grep "api" subdomains.txt
```
```
api                  (Status: 403) [Size: 118]
apis                 (Status: 403) [Size: 118]
clientapi            (Status: 403) [Size: 118]
isapi                (Status: 403) [Size: 118]
```
```
dev                  (Status: 403) [Size: 118]
dev60cgi             (Status: 403) [Size: 118]
dev2                 (Status: 403) [Size: 118]
devel                (Status: 403) [Size: 118]
develop              (Status: 403) [Size: 118]
devs                 (Status: 403) [Size: 118]
devices              (Status: 403) [Size: 118]
device               (Status: 403) [Size: 118]
developer            (Status: 403) [Size: 118]
developers           (Status: 403) [Size: 118]
devtools             (Status: 403) [Size: 118]

```