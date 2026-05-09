1. How many ports are open on the target machine?
	**4**
	```Bash
	sudo nmap -sS -sV 3.227.254.50
	```
2. Name the services running on those ports with their version
```
21/tcp    open   ftp     vsftpd 3.0.5
22/tcp    open   ssh     OpenSSH 8.7 (protocol 2.0)
80/tcp    open   http    Apache httpd 2.4.41 ((Ubuntu))
1022/tcp  open   ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
```

3. Are there know vulnerabilities for the services running?
  **Yes**

4. If there are vulnerabilities found, mention at least 2 for each service
    1) **port 22 (SSH):**
	    1. Exploit for CVE-2025-57819
	    2. Exploit for Uncontrolled Resource Consumption in Discourse
    2) **port 80 (http)**
	    1. Exploit for HTTP Request Smuggling in Apache HTTP Server
	    2. Exploit for Use of Less Trusted Source in Apache HTTP Server
    	3) **port 1022 (SSH)**
		1. Exploit for OS Command Injection in `Openbsd` `Openssh`
		2. Exploit for Unquoted Search Path or Element in `Openbsd` `Openssh`
	```
	http (port 80):
	CVE-2024-38474  9.8     https://vulners.com/cve/CVE-2024-38474
	CVE-2023-25690  9.8     https://vulners.com/cve/CVE-2023-25690
	
	SSH (port 22):
	CVE-2026-35414  8.1     https://vulners.com/cve/CVE-2026-35414
	CVE-2024-6387   8.1     https://vulners.com/cve/CVE-2024-6387
	
	ftp (port 21):
	firewall-bypass: 
	Firewall vulnerable to bypass through ftp helper. (IPv4)
	
	SSH (port 1022):
	CVE-2026-35414  8.1     https://vulners.com/cve/CVE-2026-35414
	CVE-2020-15778  7.8     https://vulners.com/cve/CVE-2020-15778
	```

6. How many files are in the ftp server's root directory?
	

There are **12** major flags hidden and a bonus flag.
Take a screenshot for all the answers you provide and how you found the flags

# Flags
![[PracticaltestFlag1.png]]
## Http source flag
By inspecting the website or following the http stream packets, we can find the ` flag{html_source_discovery}` flag.

![[PracticaltestFlag2.png]]
## Http header flag
by following the TCP stream we can find the http header flag (`flag{http_header_flag}`).

