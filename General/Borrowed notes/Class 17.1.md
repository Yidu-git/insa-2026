	
	**Blacklisting and whitelisting
	 # execution
	Exploitation
	RCE
	File Upload for different file extensions, magic bytes NULL Byte injection
	Content Type Change
	Passive File Upload ** 


## 1. File Upload Mechanics

A file upload is inherently a data transfer process. When you select a file and hit "Submit," the browser packages the file contents into an HTTP `POST` request using a special encoding format called `multipart/form-data`.

The request is broken down into segments separated by unique boundaries. Each segment contains its own mini-headers (`Content-Disposition`, `Content-Type`) followed by the raw binary or text data of the file. The backend server receives this stream of data, parses the boundaries, and decides whether to write those bytes onto its local hard drive.

---

## 2. Whitelisting vs. Blacklisting

Web developers use validation strategies to ensure that only expected files (like photos or documents) are saved to the server.

### Blacklisting 

Blacklisting is a defensive strategy where the developer creates a list of forbidden extensions (e.g., `.php`, `.exe`, `.asp`, `.html`). If the file ends with an extension on the blocklist, the server rejects it.

- **Why it fails:** It is incredibly difficult to anticipate every dangerous file type. Attackers routinely bypass blacklists by testing alternative executable extensions that the developer forgot to block (such as `.phtml`, `.php5`, or `.shtml`).
    

### Whitelisting 

Whitelisting is an explicit, restrictive strategy where the developer specifies exactly which file extensions are allowed (e.g., _only_ `.jpg`, `.jpeg`, and `.png`). Everything else is systematically rejected.

- This is a fundamental principle of "least privilege" and is vastly more secure because it leaves no room for unexpected executable types.
    

---

## 3. Passive File Upload

A **Passive File Upload** vulnerability occurs when an application allows users to upload any file type to the server, but the server does not immediately execute or parse it upon arrival. Instead, the danger lies dormant.

The file sits silently in a storage directory until one of two things happens:

1. An attacker directly browses to the path where the file is stored (e.g., `[example.com/uploads/shell.php](https://example.com/uploads/shell.php)`), forcing the web server to wake up and execute it.
    
2. Another internal server component—such as a background script, a scheduled CRON job, or a **Template Engine**—later reads and processes that stored file, triggering a secondary vulnerability like Server-Side Template Injection (SSTI).
    

---

## 4. Bypassing Restrictions (Extensions, Content-Type, Magic Bytes, Null Bytes)

When developers implement weak checks, attackers use interception proxies (like Burp Suite) to manipulate the HTTP request and sneak malicious files past the filters.

### File Extensions

If a server blocks `.php`, an attacker might try:

- **Alternative Extensions:** `.php3`, `.php4`, `.phtml`, `.phar`, or `.inc`.
    
- **Case Alternation:** `.pHp` or `.PhP` (if the underlying operating system is case-insensitive, but the regex filter is case-sensitive).
    
- **Double Extensions:** `image.png.php` (if the code splits the string incorrectly and only checks for the presence of `.png`).
    

### Content-Type Change

The `Content-Type` header tells the server what kind of data is being transmitted (e.g., `application/x-php` for a script). If the backend validation script _only_ checks this header to verify the file type, an attacker can simply intercept the upload request and manually rewrite the header to `Content-Type: image/jpeg`. The server is tricked into thinking it is receiving an innocent photo.

### Magic Bytes (File Signatures)

The extension and the `Content-Type` header are easily faked metadata. To be more thorough, some servers look at the **Magic Bytes**—the actual opening hexadecimal bytes of the file content that define its true format.

| **File Type** | **Expected Magic Bytes (Hex)**        |
| ------------- | ------------------------------------- |
| **GIF**       | `47 49 46 38 39 61` (ASCII: `GIF89a`) |
| **PNG**       | `89 50 4E 47 0D 0A 1A 0A`             |
| **JPEG**      | `FF D8 FF`                            |

To bypass this check, an attacker can prepend the string `GIF89a` to the very first line of their malicious PHP script. When the server reads the beginning of the file, it registers a valid GIF signature and allows the upload, completely ignoring the PHP payload hidden directly underneath it.

### NULL Byte Injection

Used primarily against legacy applications or older programming languages (like PHP 5.x or C/C++ based backends), this technique leverages the null character (`0x00` or `%00`).

In C-based file system functions, a null byte signifies the absolute end of a text string. An attacker uploads a file named `shell.php%00.jpg`.

1. The high-level web application validates the file extension, sees `.jpg` at the very end of the string, and clears it.
    
2. The file is handed off to the server's filesystem API to be saved.
    
3. The filesystem reads `shell.php`, hits the `%00` null byte, drops everything after it, and saves the file on disk simply as `shell.php`.
    

---

## 5. Execution vs. Exploitation vs. RCE

These three terms define the progression of a successful attack.

```
[ Exploitation ] ───────────> [ Execution ] ───────────> [ Remote Code Execution (RCE) ]
(Sneaking the web shell        (Web server running        (Total administrative control 
  past the filters)              the PHP script)            over the host OS commands)
```

### Exploitation

Exploitation is the tactical act of taking advantage of a structural flaw. In this context, exploitation is the process of using the bypasses detailed above (spoofing headers, injecting magic bytes, or finding an un-sanitized EXIF metadata field) to successfully place a malicious file onto the server's file system.

### Execution

Once the file is on the server, it has to run. **Execution** occurs when the server-side environment interprets the code inside that file. For example, if an attacker uploads a PHP web shell to an `/uploads/` directory, and the web server is configured to handle PHP files in that folder, navigating to `[example.com/uploads/shell.php](https://example.com/uploads/shell.php)` triggers the server to parse and execute those commands.

- _Note: If execution permissions are properly disabled (`noexec`) on the upload folder, the file will simply download as plain text, stopping the attack chain._
    

### Remote Code Execution (RCE)

RCE is the end goal and the ultimate impact. It means the attacker can now run arbitrary operating system commands directly on the hosting server from a remote location.

Instead of just interacting with the web application features, the attacker uses their executed file (the web shell) to run system commands like `whoami`, `id`, or `ls`. This allows them to read sensitive configuration files, compromise database credentials, or install a persistent back-door into the internal corporate network.