
---

# C2
Command and Control.
# Connecting and controlling computers with C2
To connect to a device (for this example a computer in America) we need to connect through a **C2** server. This server is used to *command and control* the target.

---

# `nmap`


---

# PowerShell downgrade attack
A **PowerShell downgrade attack** is an attack that forces PowerShell to run a script on an *older*, *less secure* version to bypass modern security measures. These attacks can be found by searching for logs with the event ID **400** witch is assigned to PowerShell. We can then sort through date and check the version to see when the downgrade occurred and to what version.

To search through logs in windows event viewer, we can find specific text with the shortcut <kbd>Ctrl</kbd> + <kbd>F</kbd>.

---
# To research
- ss
- C2
- `tcpdump`
- `terminalshark` / T-Shark
- `nmap`

12/8/2020