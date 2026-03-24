#### Topics
- What is a network
- Types of network
- IP/MAC
- Port
- UDP/TCP
# Networking
- [x] Reformat note
## What is a network
A network is a collection of computers, servers, or other devices connected together (via cables or Wi-Fi) to share data, resources, and services like internet access.
A networks type can be defined with two properties:
- Geographical coverage
- Class
IPv4 has 2^32 possible combinations of IP addresses
### Geographical coverage
**PAN** : Personal Area Network is a type of network that surrounds a **singular person**.
**LAN** : Local Area Network is a type of network that covers a house or **small area**.
**MAN** : Metropolitan Area Network is a network that covers a **metropolis**(*city*).
**WAN** : Wide Area Network covers a large area, usually a **country or continent**. It is widely called the *internet*.
### Class
![[photo_2026-03-22_11-48-36.jpg]]
<div style="font-family: sans-serif; display: flex; flex-direction: column; gap: 28px;">

  <!-- Class A -->
  <div>
    <div style="font-weight: bold; margin-bottom: 6px;">
      Class A (/8 — 255.0.0.0)
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal);">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">1–126</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">0–255</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">0–255</div>
      <div style="padding:6px;">0–255</div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal); border-top: none;">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">Host</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">Host</div>
      <div style="padding:6px;">Host</div>
    </div>
  </div>

  <!-- Class B -->
  <div>
    <div style="font-weight: bold; margin-bottom: 6px;">
      Class B (/16 — 255.255.0.0)
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal);">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">128–191</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">0–255</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">0–255</div>
      <div style="padding:6px;">0–255</div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal); border-top: none;">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal);">Host</div>
      <div style="padding:6px;">Host</div>
    </div>
  </div>

  <!-- Class C -->
  <div>
    <div style="font-weight: bold; margin-bottom: 6px;">
      Class C (/24 — 255.255.255.0)
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal);">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">192–223</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">0–255</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">0–255</div>
      <div style="padding:6px;">0–255</div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(4, 70px); text-align: center; border: 1px solid var(--text-normal); border-top: none;">
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px; border-right:1px solid var(--text-normal); background: var(--background-secondary);">Network</div>
      <div style="padding:6px;">Host</div>
    </div>
  </div>

</div>

#### Class A
4 octoate IP where the first 3 don't change
1N 3H
#### Class B
Host : 2^16 - 2 or 65534
2N2H
#### Class C
3N1H
#### Class D
#### Class E



Special IPS
- 127
- 192
- 172
- 10
- 255.255.255.255

## Exercise
What class does each IP belong to:
- 0.0.0.0 - X
- 127.0.0.0 - :LiCheck: A
- 128.0.0.0 - :LiCheck: B
- 192.0.0.0 - :LiCheck: C
- 191.255.0.0 - :LiCheck: B
- 223.255.255.0 - :LiCheck: C
- 255.255.0.0 - X
- 192.127.32.0 - :LiCheck: (C)
- 10.1.1.1 - X
- 192,168,1,1 - X (Comma)
 IP (internet protocol)
# Ports
80,433 - Http/Https
22 - SSH
__ - SMTP
20/21 - FTP
23 - Telnet
TOP ports
# TCP / UDP
![[tcp-vs-udp.svg|697]]
## TCP
- Uses 3 way handshake (syn -> syn ack -> ack)
- Integrity
Used for:
- Messaging
- Streaming
## UDP (User Datagram Protocol)
- Fast
Used for:
- Streaming
- Fast processes
- Gaming
- Network managing

# Task
Make a IP identifier using preferred programing language
Subnet identifier
IP verifier
Public vs Private IP identifier