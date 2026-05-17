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
**To cover**
- **SSTI**
- RCE
- File upload

## SSTI

### What is SSTI?

**Server-side template injection** is a vulnerability where an attacker is able to use *native template syntax* to inject a malicious payload into a template, which is then executed server-side.

**Template engines** are designed to generate web pages by ==combining fixed templates with volatile data==. Server-side template injection attacks can occur when user input is concatenated directly into a template, rather than passed in as data. This allows attackers to inject arbitrary template directives in order to manipulate the template engine, often enabling them to take complete control of the server. As the name suggests, server-side template injection payloads are delivered and evaluated server-side, potentially making them much more dangerous than a typical client-side template injection.

Template engines have a common vulnerability when used in a way they're not intended to. For example when a user inputs malicious code into a template that goes through a server, it can act as a web shell (ex: most common test for SSTI is *`{{7*7}}`* if the server returns *49* in the template it is vulnerable).

## Common template engines
### JavaScript / Node.js
- Handlebars — Logic-less templating, widely used for HTML generation.
- EJS — Lets you write plain JavaScript inside templates.
- Pug — Indentation-based HTML templating.
- Mustache — Minimal syntax and portable across languages.
- Nunjucks — Similar to Jinja2 for JavaScript projects.
### Python
- Jinja2 — The standard template engine for Flask and many Python apps.
- Tomcat
- Mako — Fast and Python-code-friendly.
- Django Templates — Built into Django.
### PHP
- Twig — Popular in Symfony and modern PHP applications.
- Blade — Default templater for Laravel.
### Java
- Thymeleaf — Common in Spring Boot applications.
- FreeMarker — Used for generating HTML, emails, configs, and docs.
- Velocity — Older but still used in enterprise systems.
### Go
- Go Templates — Built into Go (`text/template` and `html/template`).
### Ruby
- ERB — Default Ruby/Rails templating.
- Haml — Cleaner indentation-based syntax.

### Infrastructure / DevOps / Config Templating

- Helm — Uses Go templates for Kubernetes manifests.
- Terraform — Includes interpolation and template support.
- Cookiecutter — Generates project structures from templates.

### Static Site Generators / Markdown

- Liquid — Used by Jekyll and Shopify.
- Jekyll — Uses Liquid templates.
- Hugo — Uses Go templating.

### SSTI attack example

A blog site uses tomcat as a template engine, an attacker can input a payload into the site to perform a RCE. This particular payload is made for exploiting python template engines.

```
user.name}}{% import os %}{{os.system("whoami")}}
```

## What is a null byte?

**Google**
A **null byte** is a special character used in computing that has a value of zero, represented as `0x00` in hexadecimal or `\0` in programming languages. Its primary function is to serve as a marker that indicates the end of a string of text in low-level programming languages like C and C++. [1](https://medium.com/meetcyber/null-byte-attacks-explained-f032f125b919), [2](https://www.msab.com/glossary/null-byte/), [3](https://www.twingate.com/blog/glossary/null%20byte%20injection)



---
# Sources
---
## SSTI 
- [What is SSTI (portswigger.net)](https://portswigger.net/web-security/server-side-template-injection) - **portswigger.net**
- [SSTI in 100 seconds](https://www.youtube.com/watch?v=Ffeco5KB73I) - **YouTube**
- [Server-Side Template Injections Explained](https://www.youtube.com/watch?v=SN6EVIG4c-0) - **YouTube**
- [Find and Exploit Server-Side Template Injection (SSTI)](https://www.youtube.com/watch?v=x_1A9rCxREs) - **YouTube**
- [Null byte attacks are alive and well](https://portswigger.net/blog/null-byte-attacks-are-alive-and-well) - **YouTube**
- [SSTI Complete Lab Breakdown: Basic server-side template injection (code context)](https://www.youtube.com/watch?v=HC8CYztjkA8) - **YouTube**
- [Find and Exploit Server-Side Template Injection (SSTI)](https://www.youtube.com/watch?v=x_1A9rCxREs) - **YouTube**