---
cssclasses:
  - jbm-note
---
# Presentation notes
---
## Presentation 1
- Presenters: **Azaria**, **Barok**
## File upload
### What is file upload?

When a web app gives users the ability to upload any kind of file, the user can upload malicious files which contain payloads that execute scripts that give an attacker an opportunity to run **Remote Code Execution** (or *RCE*).

### How is file upload exploited?

File uploads usually follow a set of rules such as white lists that try to prevent exploits. These rules can be bypassed.

*Example*:
When a website follows a white list, it usually only checks the `Content-Type` header or the last file extension. Unfortunately for the server, both can be bypassed with `Content-Type` spoofing and manipulating the file's extensions (ex: `file.php.jpeg`).

### Why is file upload useful for attackers?

A file upload vulnerability can lead to a RCE vulnerability, lateral movement, horizontal movement and data extraction.

When a file is uploaded to a server, it is usually stored in a directory (ex: files may be uploaded in `/uploads/images/`). If this is the case, these files may be accessible directly through an API service or through a URL. This file can then be executed through **URL parameters** (*web shell*).

This can allow an attacker to gain the permissions of the server, which then allows the attacker to perform lateral movement to a different user. Then gain root access depending on the users allowed binaries.

## Presentation 2
- Presenter: **...**
## File upload
### Common uses
- document upload
- email attachment
- media sharing
- software package installation and sharing

### How is it handled
- Content validation
	- **Client** side
		- HTML
		- extensions
		- File size
		- JS
	- **Server** side
		- Extension whitelist/blacklist
		- MIME (Multipurpose Internet Mail Extensions) meta data file format
		- Webserver decides if file is executable
### Common vulnerabilities
- Extension only checks
- Weak content type verification
- Client side trust
- Executable upload directories

### Types
- Stored XSS
- HTML injection
- Information disclosure

# Research
---
- SSTI
- RCE
- File upload
- 