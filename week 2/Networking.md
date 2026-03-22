#### Topics
- What is a network
- Types of network
- IP/MAC
- Port
- UDP/TCP
# Networking
- [ ] Reformat note
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
#### Class A
4 octoate IP where the first 3 don't change
1N 3H
#### Class B
Host : 2^16 - 2 or 65534
2N2H
`![[diagram1]]`
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
## IP (internet protocol)