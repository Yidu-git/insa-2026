---
cssclasses:
  - jbm-note
---
# Web-scraping
**Web scraping**, **web harvesting**, or **web data extraction** is [data scraping](https://en.wikipedia.org/wiki/Data_scraping "Data scraping") used for [extracting data](https://en.wikipedia.org/wiki/Data_extraction "Data extraction") from [websites](https://en.wikipedia.org/wiki/Website "Website").[[1]](https://en.wikipedia.org/wiki/Web_scraping#cite_note-1) Web scraping software may directly access the [World Wide Web](https://en.wikipedia.org/wiki/World_Wide_Web "World Wide Web") using the [Hypertext Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol "Hypertext Transfer Protocol") or a web browser. While web scraping can be done manually by a software user, the term typically refers to automated processes implemented using a [bot](https://en.wikipedia.org/wiki/Internet_bot "Internet bot") or [web crawler](https://en.wikipedia.org/wiki/Web_crawler "Web crawler"). It is a form of copying in which specific data is gathered and copied from the web, typically into a central local [database](https://en.wikipedia.org/wiki/Database "Database") or [spreadsheet](https://en.wikipedia.org/wiki/Spreadsheet "Spreadsheet"), for later [retrieval](https://en.wikipedia.org/wiki/Data_retrieval "Data retrieval") or [analysis](https://en.wikipedia.org/wiki/Data_analysis "Data analysis").

---
# SQLI and XSS
## SQL Injection
- Error based
- 2nd order
### Uses
- RCE
- Privilege escalation
- Credential stealing and login
## XSS
- Blind
- DOM based
- Stored
- Reflected

---

# OWASP (Open Web Application Security Project)
## What is OWASP?

OWASP is an open project that lists the top web security vulnerabilities with each year. It collects data from CVEs and bug/vulnerability reports from top companies to asses each vulnerability.

## OWASP TOP 10
### IDOR
Insecure Direct Object Reference is an vulnerability where an API service includes an insecure reference to important objects like users or permissions without authorization or authentication.

---

# CSP (Content Security Policy)

Source: [CSP portswigger.net](https://portswigger.net/web-security/cross-site-scripting/content-security-policy)
## What is CSP (content security policy)?

CSP is a browser security mechanism that aims to mitigate XSS and some other attacks. It works by restricting the resources (such as scripts and images) that a page can load and restricting whether a page can be framed by other pages.

To enable CSP, a response needs to include an HTTP response header called `Content-Security-Policy` with a value containing the policy. The policy itself consists of one or more directives, separated by semicolons.

## Mitigating XSS attacks using CSP

The following directive will only allow scripts to be loaded from the [same origin](https://portswigger.net/web-security/cors/same-origin-policy) as the page itself:

`script-src 'self'`

The following directive will only allow scripts to be loaded from a specific domain:

`script-src https://scripts.normal-website.com`

Care should be taken when allowing scripts from external domains. If there is any way for an attacker to control content that is served from the external domain, then they might be able to deliver an attack. For example, content delivery networks (CDNs) that do not use per-customer URLs, such as `ajax.googleapis.com`, should not be trusted, because third parties can get content onto their domains.

In addition to whitelisting specific domains, content security policy also provides two other ways of specifying trusted resources: nonces and hashes:

- The CSP directive can specify a nonce (a random value) and the same value must be used in the tag that loads a script. If the values do not match, then the script will not execute. To be effective as a control, the nonce must be securely generated on each page load and not be guessable by an attacker.
- The CSP directive can specify a hash of the contents of the trusted script. If the hash of the actual script does not match the value specified in the directive, then the script will not execute. If the content of the script ever changes, then you will of course need to update the hash value that is specified in the directive.

It's quite common for a CSP to block resources like `script`. However, many CSPs do allow image requests. This means you can often use `img` elements to make requests to external servers in order to disclose CSRF tokens, for example.

Some browsers, such as Chrome, have built-in dangling markup mitigation that will block requests containing certain characters, such as raw, unencoded new lines or angle brackets.

Some policies are more restrictive and prevent all forms of external requests. However, it's still possible to [get round these restrictions by eliciting some user interaction](https://portswigger.net/research/evading-csp-with-dom-based-dangling-markup). To bypass this form of policy, you need to inject an HTML element that, when clicked, will store and send everything enclosed by the injected element to an external server.
## Mitigating dangling markup attacks using CSP

The following directive will only allow images to be loaded from the same origin as the page itself:

`img-src 'self'`

The following directive will only allow images to be loaded from a specific domain:

`img-src https://images.normal-website.com`

Note that these policies will prevent some dangling markup exploits, because an easy way to capture data with no user interaction is using an `img` tag. However, it will not prevent other exploits, such as those that inject an anchor tag with a dangling `href` attribute.

## Bypassing CSP with policy injection

You may encounter a website that reflects input into the actual policy, most likely in a `report-uri` directive. If the site reflects a parameter that you can control, you can inject a semicolon to add your own CSP directives. Usually, this `report-uri` directive is the final one in the list. This means you will need to overwrite existing directives in order to exploit this vulnerability and bypass the policy.

Normally, it's not possible to overwrite an existing `script-src` directive. However, Chrome recently introduced the `script-src-elem` directive, which allows you to control `script` elements, but not events. Crucially, this new directive allows you to [overwrite existing `script-src` directives](https://portswigger.net/research/bypassing-csp-with-policy-injection). Using this knowledge, you should be able to solve the following lab.

LAB

EXPERT[Reflected XSS protected by CSP, with CSP bypass](https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-csp-bypass)

## Protecting against clickjacking using CSP

The following directive will only allow the page to be framed by other pages from the same origin:

`frame-ancestors 'self'`

The following directive will prevent framing altogether:

`frame-ancestors 'none'`

Using content security policy to prevent clickjacking is more flexible than using the X-Frame-Options header because you can specify multiple domains and use wildcards. For example:

`frame-ancestors 'self' https://normal-website.com https://*.robust-website.com`

CSP also validates each frame in the parent frame hierarchy, whereas `X-Frame-Options` only validates the top-level frame.

Using CSP to protect against clickjacking attacks is recommended. You can also combine this with the `X-Frame-Options` header to provide protection on older browsers that don't support CSP, such as Internet Explorer.

---

# 2FA bypass
Two Factor Authentication or 2FA is a common service used by web applications to authenticate users based on a second factor (ex: email, SMS).
## 2FA Phishing

The most common form of 2FA auth is phishing where a user may be logging in to a service with a target service's account. The user is then told to input all credential details including the OTP sent to the second factor.

---

# Hash cracking
Most IDOR vulnerabilities also allow hash cracking when using a weak hash. 

*Example* : When an IDOR allows any user to look at other user details like password hash, if that hash has no hash key or has a weak password, the password can be hacked with tools such as hash hack.

---

# RCE (Remote code execution)

## What is RCE?

Remote Code Execution is a vulnerability class that allows an attacker to run arbitrary code on a target system from a remote location without physical access or an existing account on the server.

## Dangers of RCE

- Data exfiltration
- Credential theft
- Lateral Movement
- Ransomware
- Privilege Escalation
- Direct access to server software

## Types of RCE

- Malicious file upload
- Command & Code Injection
- Insecure Deserialization


---

# File upload vulnerabilities
Covering :
- File upload functionality
- Common use cases
- What increases attack surface
- How file handling works

**MIME** Type : meta data
**Extension** : suffix (`.exe`, `.php`, `.js`)
**Storage Path** : Where the file sits
## What is File upload functionality?
### Common use cases

- Profile pictures
- Document uploads
- Media Sharing
- Email
- Software packages
- Text
### What increases the attack surface

- Untrusted files enter the surface env
- Filenames may contain path traversal sequences
- MIME types are easily spoofed by attackers
- Executable files can be masquerade as images
- Storage paths may be web-accessible
- Insufficient validation at client side

## Important server-side processing

- Server decides weather file is executable
- File usually gets renamed when uploaded
## Validation failures

- Extension-ONLY checks
- Weak Content-Type verification
- Client-side validation trust
- Executable upload directories

## Stored XSS + File Upload

Because of how :TiFileTypeSvg:SVG files are saved, :TiFileTypeSvg:SVG or :SiHtml5: HTML files can be uploaded that contain `<script></script>` payloads. This can lead to Cookie hijacking, keystroke logging and token stealing.

*Example* :
An SVG file containing a payload is uploaded to a site:
```XML
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    alert(document.cookie)
  </script>
</svg>
```
When this file is uploaded, whoever opens this SVG file receives an alert message containing their cookie.

## HTML Injection

HTML injection is different form XSS in its ability to become the malicious page, served under the app's trusted origin. This removes the use of reflected/stored XSS.

## Information Disclosure

Web accessible directories allow for direct URL enumeration. Attackers can guess paths to access other users files. Misconfigured Apache/Nginx serves a listing of all uploaded files. Attacker browses the entire contents of the upload folder.

## Path traversal

When a server uses a user supplied filename directly in a file path without proper sanitization, an attacker can craft filenames containing directory traversal sequences.

This could be used to eventually execute injected malicious files.

## Web shell

**Web shell** : A script uploaded to a server, that once accessible via browser provides an attacker with a command-line control of the underlying OS.

## Simple :SiPhp: PHP payload

```php
<?php
if(isset($_GET('cmd'))) {
  $cmd = $_GET('cmd');
  echo (system($cmd));
}
?>
```

One liner:
```PHP
<?php if(isset($_GET('cmd'))) { $cmd = $_GET('cmd'); echo (system($cmd)); } ?>
```
## Real-world RCE CVEs

- 2017
- 2019
- 2021
- 2022

## Prevention

- Allow-list Extension Validation
- Randomized Filenames
- Non-Executable Storage
- File Type Verification
- Whitelist over blacklist

## Common tactics

- Double extensions
- Case manipulation
- Content-Type spoofing
- Polyglot Files
- Archive based bypass (.zip)

---

# User privilege escalation
Most unprivileged users on a still have access to certain binaries that may be vulnerable. Using these vulnerable binaries (such as python3), we can use tools such as `GTFObinaries` to get root access.