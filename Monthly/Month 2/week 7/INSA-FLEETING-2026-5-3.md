# Rate limiting & proxies
To protect servers from brute force attacks, most services use a rate limit. A **rate limit** is a limit of how many requests a server will respond to from a specific source. To evade rate limits, hackers use multiple proxies and services.

**Proxy** is an external machine which a client connects to that sends requests that the machine forwards. It acts as a node between a service and client.

[[Drawing 2026-05-03 14.11.12.excalidraw]]

**Proxy chain** : a chain of proxies that connect to each other. They contain *entry nodes*, *exit nodes* and *middle relay nodes*.

# Network Service Enumeration & common web vulnerabilities

## Banner grabbing
**Banner grabbing** : collecting info on the version and service from open ports.
Tools :
- `netcat`
## Service fingerprinting
- Identifies what is running on a port
- probes for responses


# Sub finder
```Bash
subfinder -d https://vulnbank.org -v
```
