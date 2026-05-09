# intercepting
- `Burpsuite`
- `Caido`
- `Zap`
The purpose of these tools is to intercept http requests and try to find any web-vulnerabilities.

# OWASP
**OWASP** : Open Web App Security
**OWASP for mobile** :

## Broken access control
- *IDOR*
- *Brute force*
- *SQL injection*

## Privilege escalation
Is an attack where a user escalates or gains access to higher privileges. This vulnerability can be dangerous when paired with other vulnerabilities like Brocken access control.

# CVE (Common Vulnerability Enumeration)
Is an open list of common vulnerabilities.
# IDOR (Insecure Direct Object Reference)
An **IDOR** vulnerability where a user can access other user data by abusing the service API.
#### Example scenario
A user uses a service that *GET*s the user profile through the following API call:
```
GET /profile/?user_id=1023
```
This user edits the API call to change the *`user_id`* to 1024 to get another users profile.
####
This attack can also be done by editing the sites cookie.

React.js http header IDOR : **`nextaction`**
This header is used for redirects and post login(onboarding) to take the next course of action.

# IDOR Testing
When pen testing for IDOR vulnerabilities always create two accounts to try and access the second persons account.

# Password (Auth) attacks
- **Brute force** : Is attempting multiple passwords for a particular user
- **Credential stuffing** : Credential stuffing is the automated injection of stolen username and password pairs (“credentials”) in to website login forms, in order to fraudulently gain access to user accounts.
- **Password spraying** : The basics of a password spraying attack involve a [threat actor](https://www.crowdstrike.com/en-us/cybersecurity-101/threat-intelligence/threat-actor/) using a single common password against multiple accounts on the same application. This avoids the account lockouts that typically occur when an attacker uses a brute force attack on a single account by trying many passwords. Password spraying is particularly effective against businesses that participate in password sharing.

## Common defense tactics
- 2FA : protecting a password or account through a third party (email, SMS).
- IP rate limiting : Rate limiting requests form a particular IP

**OTP**

# Tips
- Always check for implementation error.
- When forced to crack authentications, always look for social engineering paths as the human is always the weakest link in any system.

# HTTP Cookies
- HTTP STRICT: Only allows cookies to be sent to the same site that initiated the cookie.

# Injection
## SQL injection
Using a common vulnerability in sites that don't sanitize user input. This particular exploit takes advantage of the SQL syntax

### SQL syntax
- **SELECT** read/retrieve
	- *`SELECT name, age FROM employees`*
- **UPDATE** : updates a row
- **DELETE** : deletes rows
- **CREATE TABLE** : Creates table
- **AND**, **OR**,**=** Logical params
	- *`SELECT * WHERE name = 'jhon' AND password = 'jhon@2001' `*
- **`-- `** : comment

#### Simple SQL injection scenario
When you input your username and password into a site, the logic looks something like this (For this example a Node.js backend is used) :
```JS
const Login(username,password) {
	const query = ``;
	try {
	    const [result] = await pool.query();
	    const [rows] = await pool.query("SELECT * FROM users WHERE username = ? AND passwrod = ?", [
      username, password
    ]);
    return rows[0];
  } catch (error) {
	    throw new error(error);
  }
}
```
If we input our password and username normally (*`jhon`*, *`jhon@2001`*) into a login form, the SQL query should look like the following
```SQL
SELECT * WHERE username = 'jhon' AND password = 'jhon@2001' 
```
While this works on its own, if we don't *sanitize* user data, this logic can be vulnerable to a SQL injection where the users enters **`' OR 1=1 --`** which ends the comment when searching for the username and comments out the query that checks the password.
```SQL
SELECT * FROM users WHERE username = 'jhon' OR 1=1 -- 'AND password = 'jhon@2001
```
 - where to check for SQLI
 - Detection
 - Exploitation
### Tools
- SQL map

### Prevention
- User input sanitization (ex **regex** filters)
- 
#### Principles
- Always assume user input is dirty
- Always sanitize user input
- Never allow users to have access to inputs that they don't need

## XSS
- DOM
- Reflected
- Stored
- Blind
### [Reflected XSS](https://owasp.org/www-community/attacks/xss/#reflected-xss-attacks) (AKA Non-Persistent or Type I)

Reflected XSS occurs when user input is immediately returned by a web application in an error message, search result, or any other response that includes some or all of the input provided by the user as part of the request, without that data being made safe to render in the browser, and without permanently storing the user provided data. In some cases, the user provided data may never even leave the browser (see DOM Based XSS below).

### [Stored XSS](https://owasp.org/www-community/attacks/xss/#stored-xss-attacks) (AKA Persistent or Type II)

Stored XSS generally occurs when user input is stored on the target server, such as in a database, in a message forum, visitor log, comment field, etc. And then a victim is able to retrieve the stored data from the web application without that data being made safe to render in the browser. With the advent of HTML5, and other browser technologies, we can envision the attack payload being permanently stored in the victim’s browser, such as an HTML5 database, and never being sent to the server at all.

### [DOM Based XSS](https://owasp.org/www-community/attacks/DOM_Based_XSS) (AKA Type-0)

DOM Based XSS (or as it is called in some texts, “type-0 XSS”) is an XSS attack wherein the attack payload is executed as a result of modifying the DOM “environment” in the victim’s browser used by the original client side script, so that the client side code runs in an “unexpected” manner. That is, the page itself (the HTTP response that is) does not change, but the client side code contained in the page executes differently due to the malicious modifications that have occurred in the DOM environment.

### [Blind XSS](https://owasp.org/www-community/attacks/) (AKA Type-III)

Blind XSS is an XSS attack where we are not able to see the results of the attack or view it.

## Detection
We can test XSS vulnerabilities by simply testing what inputs gets blocked by the site.
- XSS CHEAT SHEET
- Analyzing source code

