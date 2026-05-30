---
cssclasses:
  - jbm-note
Date: 2026-05-22
tags:
  - THMChallenge
---
# ... Challenge

| **Target**            | *Try hack me machine(room: biohazard)* |
| --------------------- | -------------------------------------- |
| Date                  | 22/5/2026                              |
| Main attack type      | ...                                    |
| Secondary attack type | ...                                    |
| Tools:                | ...                                    |
| Criticality:          | **...**                                |

---
# **RESULTS**
---
## Flags found
- *emblem{fec832623ea498e20bf4fe1821d58727}*
- *lock_pick{037b35e2ff90916a9abf99129c8e1837}*
- *music_sheet{362d72deaf65f5bdc63daece6a1f676e}*
- *gold_emblem{58a8c41a9d08b8a4e38d02a4d7ff4843}*
- *shield_key{48a7a9227cd7eb89f0a062590798cbac}*
- *blue_jewel{e1d457e96cac640f863ec7bc475d48aa}*
- *helmet_key{458493193501d2b94bbab2e727f8db4b}*
- *root : 3c5794a00dc56c35f2bf096571edf3bf*
- *you_cant_hide_forever*

- `cGxhbnQ0Ml9jYW`
- `5fYmVfZGVzdHJveV9`
- `3aXRoX3Zqb2x0`
- `cGxhbnQ0Ml9jYW5fYmVfZGVzdHJveV93aXRoX3Zqb2x0`
- `plant42_can_be_destroy_with_vjolt`

- *SSH password: T_virus_rules*
- *SSH user: umbrella_guest*
- *weasker*
- *`stars_members_are_my_guinea_pig`*
- ``plant42_can_be_destroy_with_vjolt``
- `stars_members_are_my_guinea_pig`

- **`pass: dustbin_plastic`**
- `the_great_shield_key`
- `ss: you_cant_hide_forever`
- `FTP user: hunter, FTP pass: you_cant_hide_forever`

---
# Preparation
---
## Getting the PHP payload
...

---
# Initial investigation/enumeration
---
## **Enumeration**
### NMAP
```bash
sudo nmap -sS -sV 10.82.163.247 -oA scans
```
```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```

## GOBUSTER
...

## **Vulnerability scanning**
Not needed.

---
# Exploiting and  Investigation
---
## First
