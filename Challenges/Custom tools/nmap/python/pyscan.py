#!/usr/bin/env python3
"""
pyscan.py — Python Network Scanner
Implements Nmap-like scanning from scratch using raw sockets and the stdlib.

Scan types : TCP Connect · SYN Stealth · Xmas · NULL · FIN · UDP
Features   : Host discovery · service banner grab · OS fingerprinting (TTL)
             Port-state detection · rich TUI · JSON + text export

Requirements: Python 3.9+, rich      (pip install rich)
Root / sudo : Required for SYN, Xmas, NULL, FIN, UDP scans.
              Connect scan works without root.
"""

import argparse
import datetime
import ipaddress
import json
import os
import queue
import random
import select
import socket
import struct
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

try:
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (BarColumn, MofNCompleteColumn, Progress,
                               SpinnerColumn, TextColumn)
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Missing dependency. Run:  pip install rich")
    sys.exit(1)

console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# TCP flag bitmasks
F_FIN = 0x01
F_SYN = 0x02
F_RST = 0x04
F_PSH = 0x08
F_ACK = 0x10
F_URG = 0x20

TOP_100_PORTS = [
    7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111,
    113, 119, 135, 139, 143, 179, 199, 389, 427, 443, 444, 445, 465, 513,
    514, 515, 543, 544, 548, 554, 587, 631, 873, 990, 993, 995, 1025, 1026,
    1027, 1028, 1029, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121,
    2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101,
    5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000,
    8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152,
    49153, 49154, 49155, 49156, 49157, 6379, 11211, 27017,
]

SERVICE_MAP = {
    7: "echo",         9: "discard",   13: "daytime",   21: "ftp",
    22: "ssh",         23: "telnet",   25: "smtp",       26: "rsftp",
    37: "time",        53: "dns",      79: "finger",     80: "http",
    81: "hosts2-ns",   88: "kerberos", 110: "pop3",      111: "rpcbind",
    113: "ident",      119: "nntp",    135: "msrpc",     139: "netbios-ssn",
    143: "imap",       179: "bgp",     199: "smux",      389: "ldap",
    443: "https",      445: "smb",     465: "smtps",     513: "login",
    514: "shell",      515: "printer", 548: "afp",       554: "rtsp",
    587: "submission", 631: "ipp",     873: "rsync",     990: "ftps",
    993: "imaps",      995: "pop3s",   1433: "ms-sql",   1720: "h.323",
    1723: "pptp",      1900: "upnp",   2049: "nfs",      2121: "ftp-proxy",
    3000: "ppp",       3128: "squid",  3306: "mysql",    3389: "rdp",
    5432: "postgresql",5900: "vnc",    6000: "x11",      6379: "redis",
    8000: "http-alt",  8008: "http",   8080: "http-proxy",8443: "https-alt",
    8888: "http-alt",  9100: "jetdirect",9999: "abyss",  10000: "webmin",
    11211: "memcache", 27017: "mongodb",
}

# TTL → OS fingerprint
OS_TTL = [
    ((56, 68),   "Linux (kernel 2.4+)"),
    ((62, 66),   "macOS / FreeBSD"),
    ((124, 132), "Windows"),
    ((252, 256), "Cisco / Solaris"),
    ((28, 34),   "Linux (custom TTL)"),
]

TIMING = {
    "T0": {"workers": 1,   "timeout": 5.0,  "label": "Paranoid"},
    "T1": {"workers": 3,   "timeout": 3.0,  "label": "Sneaky"},
    "T2": {"workers": 10,  "timeout": 2.0,  "label": "Polite"},
    "T3": {"workers": 20,  "timeout": 1.0,  "label": "Normal"},
    "T4": {"workers": 50,  "timeout": 0.5,  "label": "Aggressive"},
    "T5": {"workers": 100, "timeout": 0.3,  "label": "Insane"},
}

OUTPUT_DIR = Path("pyscan_results")
OUTPUT_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────────────────────────────────────

def is_root() -> bool:
    return hasattr(os, "geteuid") and os.geteuid() == 0


def get_local_ip(target: str) -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def resolve(target: str) -> Optional[str]:
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def parse_targets(spec: str) -> list[str]:
    targets: list[str] = []
    for part in spec.split(","):
        part = part.strip()
        try:
            net = ipaddress.ip_network(part, strict=False)
            if net.num_addresses == 1:
                targets.append(str(net.network_address))
            else:
                targets.extend(str(h) for h in net.hosts())
        except ValueError:
            ip = resolve(part)
            if ip:
                targets.append(ip)
            else:
                console.print(f"[red]Cannot resolve: {part}[/]")
    return targets


def parse_ports(spec: str, top: int = 0) -> list[int]:
    if top:
        return sorted(TOP_100_PORTS[:min(top, len(TOP_100_PORTS))])
    if spec.strip() == "-":
        return list(range(1, 65536))
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            lo_i = int(lo) if lo else 1
            hi_i = int(hi) if hi else 65535
            ports.update(range(lo_i, hi_i + 1))
        elif part:
            ports.add(int(part))
    return sorted(ports)


def guess_os(ttl: int) -> str:
    for (lo, hi), name in OS_TTL:
        if lo <= ttl < hi:
            return name
    return "Unknown"


def safe_filename(s: str) -> str:
    import re
    return re.sub(r"[^\w\-.]", "_", s)


# ─────────────────────────────────────────────────────────────────────────────
# PACKET CRAFTING  (IP + TCP / UDP headers from scratch)
# ─────────────────────────────────────────────────────────────────────────────

def _checksum(data: bytes) -> int:
    """RFC 1071 Internet checksum."""
    if len(data) % 2:
        data += b"\x00"
    s = sum((data[i] << 8) + data[i + 1] for i in range(0, len(data), 2))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF


def craft_tcp_packet(src_ip: str, dst_ip: str, src_port: int, dst_port: int,
                     flags: int, seq: int = 0, ack_seq: int = 0,
                     window: int = 64240) -> bytes:
    """Build a full IPv4 + TCP packet with correct checksums."""
    if seq == 0:
        seq = random.randint(1_000_000, 4_200_000_000)

    # ── TCP header (checksum = 0 initially) ──────────────────────────────
    tcp = struct.pack("!HHLLBBHHH",
        src_port, dst_port,
        seq, ack_seq,
        0x50,    # data offset = 5 (20 bytes), reserved nibble = 0
        flags,
        window,
        0, 0     # checksum placeholder, urgent pointer
    )

    # TCP checksum uses pseudo-header
    pseudo = struct.pack("!4s4sBBH",
        socket.inet_aton(src_ip),
        socket.inet_aton(dst_ip),
        0, socket.IPPROTO_TCP, len(tcp)
    )
    csum = _checksum(pseudo + tcp)
    tcp = struct.pack("!HHLLBBHHH",
        src_port, dst_port, seq, ack_seq, 0x50, flags, window, csum, 0)

    # ── IP header (kernel fills total_len and ip_checksum on Linux) ───────
    ip_id = random.randint(1, 65535)
    ip = struct.pack("!BBHHHBBH4s4s",
        0x45,   # version=4, IHL=5
        0,      # DSCP/ECN
        0,      # total length  (kernel fills)
        ip_id,
        0x4000, # DF=1, MF=0, offset=0
        64,     # TTL
        socket.IPPROTO_TCP,
        0,      # checksum      (kernel fills)
        socket.inet_aton(src_ip),
        socket.inet_aton(dst_ip),
    )
    return ip + tcp


def craft_udp_packet(src_ip: str, dst_ip: str,
                     src_port: int, dst_port: int,
                     payload: bytes = b"") -> bytes:
    """Build IPv4 + UDP packet."""
    udp_len = 8 + len(payload)
    pseudo = struct.pack("!4s4sBBH",
        socket.inet_aton(src_ip),
        socket.inet_aton(dst_ip),
        0, socket.IPPROTO_UDP, udp_len
    )
    udp_hdr = struct.pack("!HHHH", src_port, dst_port, udp_len, 0)
    csum = _checksum(pseudo + udp_hdr + payload)
    udp = struct.pack("!HHHH", src_port, dst_port, udp_len, csum) + payload

    ip = struct.pack("!BBHHHBBH4s4s",
        0x45, 0, 0, random.randint(1, 65535),
        0x4000, 64, socket.IPPROTO_UDP, 0,
        socket.inet_aton(src_ip), socket.inet_aton(dst_ip),
    )
    return ip + udp


def parse_ip_tcp(data: bytes) -> Optional[dict]:
    """Parse raw IP+TCP packet. Returns dict or None."""
    if len(data) < 20:
        return None
    iph = struct.unpack("!BBHHHBBH4s4s", data[:20])
    ihl = (iph[0] & 0x0F) * 4
    if len(data) < ihl + 20:
        return None
    tcph = struct.unpack("!HHLLBBHHH", data[ihl:ihl + 20])
    return {
        "ttl":      iph[5],
        "src_ip":   socket.inet_ntoa(iph[8]),
        "tcp_sport": tcph[0],  # target's port
        "tcp_dport": tcph[1],  # our src port
        "flags":    tcph[5],
        "window":   tcph[6],
    }


def parse_ip_icmp(data: bytes) -> Optional[dict]:
    """Parse ICMP packet. Returns dict or None."""
    if len(data) < 20:
        return None
    iph = struct.unpack("!BBHHHBBH4s4s", data[:20])
    ihl = (iph[0] & 0x0F) * 4
    if len(data) < ihl + 8:
        return None
    icmph = struct.unpack("!BBHHH", data[ihl:ihl + 8])
    return {
        "type":    icmph[0],
        "code":    icmph[1],
        "src_ip":  socket.inet_ntoa(iph[8]),
        "payload": data[ihl + 8:],
    }


# ─────────────────────────────────────────────────────────────────────────────
# PACKET DISPATCHER  (one background thread reads all incoming raw TCP packets
#                     and routes them to per-source-port queues)
# ─────────────────────────────────────────────────────────────────────────────

class PacketDispatcher:
    """Background thread that fans-out received raw TCP packets."""

    def __init__(self, raw_sock: socket.socket):
        self._sock = raw_sock
        self._lock = threading.Lock()
        self._queues: dict[int, queue.Queue] = {}
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def register(self, src_port: int) -> queue.Queue:
        q: queue.Queue = queue.Queue()
        with self._lock:
            self._queues[src_port] = q
        return q

    def unregister(self, src_port: int) -> None:
        with self._lock:
            self._queues.pop(src_port, None)

    def _loop(self) -> None:
        while self._running:
            try:
                ready = select.select([self._sock], [], [], 0.05)
                if not ready[0]:
                    continue
                data, _ = self._sock.recvfrom(65535)
                pkt = parse_ip_tcp(data)
                if pkt is None:
                    continue
                with self._lock:
                    q = self._queues.get(pkt["tcp_dport"])
                if q is not None:
                    q.put(pkt)
            except Exception:
                pass

    def stop(self) -> None:
        self._running = False
        self._thread.join(timeout=1.0)


# Global dispatcher (initialised lazily when root scans are requested)
_dispatcher: Optional[PacketDispatcher] = None
_raw_tcp_sock: Optional[socket.socket] = None
_disp_lock = threading.Lock()


def get_dispatcher() -> Optional[PacketDispatcher]:
    global _dispatcher, _raw_tcp_sock
    with _disp_lock:
        if _dispatcher is not None:
            return _dispatcher
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                              socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            _raw_tcp_sock = s
            _dispatcher = PacketDispatcher(s)
            return _dispatcher
        except PermissionError:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# HOST DISCOVERY
# ─────────────────────────────────────────────────────────────────────────────

def ping_tcp(ip: str, port: int = 80, timeout: float = 1.0) -> bool:
    """TCP-based host-up check (no root needed)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        # connect succeeded or connection refused both mean host is up
        return result in (0, 111)
    except Exception:
        return False


def ping_icmp(ip: str, timeout: float = 1.0) -> tuple[bool, int]:
    """ICMP echo ping. Returns (alive, ttl). Requires root."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                          socket.IPPROTO_ICMP)
        s.settimeout(timeout)
        ident = random.randint(1, 65535)
        seq = 1
        # ICMP echo request: type=8, code=0
        header = struct.pack("!BBHHH", 8, 0, 0, ident, seq)
        payload = b"pyscan"
        csum = _checksum(header + payload)
        packet = struct.pack("!BBHHH", 8, 0, csum, ident, seq) + payload
        s.sendto(packet, (ip, 0))
        start = time.time()
        while time.time() - start < timeout:
            ready = select.select([s], [], [], timeout - (time.time() - start))
            if not ready[0]:
                break
            data, _ = s.recvfrom(1024)
            # IP header is 20 bytes, ICMP starts at byte 20
            if len(data) >= 28:
                iph = struct.unpack("!BBHHHBBH4s4s", data[:20])
                icmp_type = data[20]
                if icmp_type == 0:  # echo reply
                    return True, iph[5]  # iph[5] = TTL
        s.close()
    except Exception:
        pass
    return False, 0


# ─────────────────────────────────────────────────────────────────────────────
# TCP CONNECT SCAN  (no root needed)
# ─────────────────────────────────────────────────────────────────────────────

def scan_connect(ip: str, port: int, timeout: float) -> str:
    """Full TCP connect scan. Returns 'open', 'closed', or 'filtered'."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()
        if result == 0:
            return "open"
        elif result in (111, 10061):  # ECONNREFUSED
            return "closed"
        else:
            return "filtered"
    except socket.timeout:
        return "filtered"
    except Exception:
        return "filtered"


# ─────────────────────────────────────────────────────────────────────────────
# RAW TCP SCANS  (SYN · Xmas · NULL · FIN  — requires root)
# ─────────────────────────────────────────────────────────────────────────────

def _raw_tcp_probe(ip: str, port: int, flags: int,
                   src_ip: str, timeout: float,
                   dispatcher: PacketDispatcher) -> Optional[dict]:
    """Send a raw TCP probe and return the first matching response packet."""
    src_port = random.randint(40000, 59999)
    pkt = craft_tcp_packet(src_ip, ip, src_port, port, flags)

    q = dispatcher.register(src_port)
    try:
        # Send via a short-lived raw socket
        with socket.socket(socket.AF_INET, socket.SOCK_RAW,
                           socket.IPPROTO_RAW) as tx:
            tx.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            tx.sendto(pkt, (ip, 0))

        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                pkt_recv = q.get(timeout=deadline - time.time())
                if pkt_recv["src_ip"] == ip and pkt_recv["tcp_sport"] == port:
                    return pkt_recv
            except queue.Empty:
                break
    finally:
        dispatcher.unregister(src_port)
    return None


def scan_syn(ip: str, port: int, src_ip: str,
             timeout: float, dispatcher: PacketDispatcher) -> tuple[str, int]:
    """SYN stealth scan. Returns (state, ttl)."""
    resp = _raw_tcp_probe(ip, port, F_SYN, src_ip, timeout, dispatcher)
    if resp is None:
        return "filtered", 0
    f = resp["flags"]
    if (f & (F_SYN | F_ACK)) == (F_SYN | F_ACK):
        return "open", resp["ttl"]
    if f & F_RST:
        return "closed", resp["ttl"]
    return "filtered", resp["ttl"]


def scan_stealth(ip: str, port: int, flags: int, src_ip: str,
                 timeout: float, dispatcher: PacketDispatcher) -> str:
    """Xmas / NULL / FIN scan (RFC 793 trick scans).
    Rules (RFC 793, non-Windows):
      RST received   → closed
      No response    → open | filtered
    """
    resp = _raw_tcp_probe(ip, port, flags, src_ip, timeout, dispatcher)
    if resp is None:
        return "open|filtered"
    if resp["flags"] & F_RST:
        return "closed"
    return "open|filtered"


# ─────────────────────────────────────────────────────────────────────────────
# UDP SCAN  (requires root for ICMP detection)
# ─────────────────────────────────────────────────────────────────────────────

def scan_udp(ip: str, port: int, src_ip: str, timeout: float) -> str:
    """UDP scan with ICMP Port-Unreachable detection (root) or fallback."""
    # ── Root path: send raw UDP, sniff ICMP response ────────────────────
    if is_root():
        try:
            icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                      socket.IPPROTO_ICMP)
            icmp_sock.settimeout(timeout)
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                     socket.IPPROTO_RAW)
            udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            src_port = random.randint(40000, 59999)
            pkt = craft_udp_packet(src_ip, ip, src_port, port)
            udp_sock.sendto(pkt, (ip, 0))
            udp_sock.close()

            deadline = time.time() + timeout
            while time.time() < deadline:
                rem = deadline - time.time()
                if rem <= 0:
                    break
                ready = select.select([icmp_sock], [], [], rem)
                if not ready[0]:
                    break
                data, addr = icmp_sock.recvfrom(1024)
                if addr[0] != ip:
                    continue
                icmp = parse_ip_icmp(data)
                if icmp and icmp["type"] == 3:
                    # ICMP Destination Unreachable
                    if icmp["code"] == 3:
                        # Port Unreachable → closed
                        icmp_sock.close()
                        return "closed"
                    else:
                        # Other unreachable codes → filtered
                        icmp_sock.close()
                        return "filtered"
            icmp_sock.close()
            return "open|filtered"
        except Exception:
            pass

    # ── Non-root fallback: use regular UDP socket ────────────────────────
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        s.sendto(b"\x00" * 4, (ip, port))
        try:
            s.recvfrom(1024)
            return "open"
        except socket.timeout:
            return "open|filtered"
        except ConnectionRefusedError:
            return "closed"
        finally:
            s.close()
    except Exception:
        return "open|filtered"


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE DETECTION  (banner grab + port-map lookup)
# ─────────────────────────────────────────────────────────────────────────────

# Probes to send to specific services to elicit a banner
SERVICE_PROBES = {
    80:    b"HEAD / HTTP/1.0\r\nHost: pyscan\r\n\r\n",
    8080:  b"HEAD / HTTP/1.0\r\nHost: pyscan\r\n\r\n",
    8000:  b"HEAD / HTTP/1.0\r\nHost: pyscan\r\n\r\n",
    8443:  b"HEAD / HTTP/1.0\r\nHost: pyscan\r\n\r\n",
    443:   b"HEAD / HTTP/1.0\r\nHost: pyscan\r\n\r\n",
    21:    b"",   # FTP sends banner immediately
    22:    b"",   # SSH sends banner immediately
    25:    b"",   # SMTP sends banner
    110:   b"",   # POP3
    143:   b"",   # IMAP
    3306:  b"",   # MySQL
    5432:  b"",   # PostgreSQL
    6379:  b"PING\r\n",
    27017: b"",
}


def grab_banner(ip: str, port: int, timeout: float = 2.0) -> str:
    """Connect and read the service banner. Returns version string or ''."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))

        probe = SERVICE_PROBES.get(port, b"")
        if probe:
            s.sendall(probe)

        s.settimeout(1.0)
        try:
            banner = s.recv(1024)
        except socket.timeout:
            banner = b""
        s.close()

        text = banner.decode("utf-8", errors="ignore").strip()
        return _parse_banner(port, text)
    except Exception:
        return ""


def _parse_banner(port: int, raw: str) -> str:
    """Extract a clean version string from a raw service banner."""
    if not raw:
        return ""
    lines = raw.splitlines()
    first = lines[0] if lines else ""

    # SSH: "SSH-2.0-OpenSSH_9.3p2 Ubuntu-1"
    if first.startswith("SSH-"):
        parts = first.split("-", 2)
        return parts[2] if len(parts) > 2 else first

    # HTTP: look for Server header
    for line in lines:
        if line.lower().startswith("server:"):
            return line.split(":", 1)[1].strip()

    # FTP: "220 ProFTPD 1.3.5 Server"
    if first.startswith("220"):
        return first[3:].strip()

    # SMTP
    if first.startswith("220"):
        return first[3:].strip()

    # Redis: "+PONG" or error
    if first in ("+PONG", "+OK"):
        return "Redis"

    # MySQL: starts with protocol version byte (non-printable) but contains version
    import re
    m = re.search(r"(\d+\.\d+\.\d+[\w.-]*)", raw)
    if m:
        return m.group(1)

    return first[:60] if first else ""


# ─────────────────────────────────────────────────────────────────────────────
# SCAN ENGINE
# ─────────────────────────────────────────────────────────────────────────────

class ScanResult:
    __slots__ = ("port", "protocol", "state", "service", "version", "ttl")

    def __init__(self, port: int, protocol: str = "tcp",
                 state: str = "closed", service: str = "",
                 version: str = "", ttl: int = 0):
        self.port = port
        self.protocol = protocol
        self.state = state
        self.service = service
        self.version = version
        self.ttl = ttl


class Scanner:
    SCAN_TYPES = ("connect", "syn", "xmas", "null", "fin", "udp")

    # Map scan type → TCP flags for stealth scans
    FLAG_MAP = {
        "xmas": F_FIN | F_PSH | F_URG,
        "null": 0,
        "fin":  F_FIN,
    }

    def __init__(self, target_ip: str, ports: list[int],
                 scan_type: str = "connect",
                 timing: str = "T3",
                 service_detect: bool = False,
                 os_detect: bool = False,
                 no_ping: bool = False,
                 verbose: bool = False):
        self.target = target_ip
        self.ports = ports
        self.scan_type = scan_type
        self.timing_cfg = TIMING.get(timing, TIMING["T3"])
        self.timeout = self.timing_cfg["timeout"]
        self.workers = self.timing_cfg["workers"]
        self.service_detect = service_detect
        self.os_detect = os_detect
        self.no_ping = no_ping
        self.verbose = verbose
        self.src_ip = get_local_ip(target_ip)
        self.results: list[ScanResult] = []
        self.os_guess: str = ""
        self.host_up: bool = False
        self.ttl_sample: int = 0
        self._dispatcher: Optional[PacketDispatcher] = None

    # ── Public entry point ───────────────────────────────────────────────────

    def run(self) -> list[ScanResult]:
        # Host discovery
        if not self.no_ping:
            self.host_up = self._discover()
            if not self.host_up:
                return []
        else:
            self.host_up = True

        # Raw socket setup for root scans
        if self.scan_type in ("syn", "xmas", "null", "fin"):
            if not is_root():
                console.print(
                    Panel("[yellow]Root required for SYN/Xmas/NULL/FIN scans. "
                          "Falling back to connect scan.[/]",
                          border_style="yellow"))
                self.scan_type = "connect"
            else:
                self._dispatcher = get_dispatcher()
                if self._dispatcher is None:
                    console.print(
                        Panel("[yellow]Could not open raw socket. "
                              "Falling back to connect scan.[/]",
                              border_style="yellow"))
                    self.scan_type = "connect"

        # Run scan with progress bar
        self.results = self._scan_ports()

        # OS detection
        if self.os_detect and self.ttl_sample:
            self.os_guess = guess_os(self.ttl_sample)

        return self.results

    # ── Host discovery ───────────────────────────────────────────────────────

    def _discover(self) -> bool:
        if is_root():
            alive, ttl = ping_icmp(self.target, self.timeout)
            if alive:
                self.ttl_sample = ttl
                return True
        # TCP fallback: try ports 80 and 443
        for p in (80, 443, 22, 8080):
            if ping_tcp(self.target, p, self.timeout):
                return True
        return False

    # ── Port scanning ────────────────────────────────────────────────────────

    def _scan_ports(self) -> list[ScanResult]:
        results: list[ScanResult] = []
        lock = threading.Lock()

        with Progress(
            SpinnerColumn(style="green"),
            TextColumn("[green]{task.description}"),
            BarColumn(bar_width=30, style="green", complete_style="bright_green"),
            MofNCompleteColumn(),
            TextColumn("[dim]{task.fields[found]} open"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(
                f"Scanning {self.target} ({self.scan_type.upper()})",
                total=len(self.ports), found=0
            )

            def scan_one(port: int) -> ScanResult:
                return self._scan_port(port)

            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                futures = {pool.submit(scan_one, p): p for p in self.ports}
                for fut in as_completed(futures):
                    r = fut.result()
                    with lock:
                        results.append(r)
                        open_count = sum(1 for x in results if x.state == "open")
                        progress.update(task, advance=1, found=open_count)

        return sorted(results, key=lambda r: r.port)

    def _scan_port(self, port: int) -> ScanResult:
        st = self.scan_type
        proto = "udp" if st == "udp" else "tcp"
        r = ScanResult(port=port, protocol=proto,
                       service=SERVICE_MAP.get(port, ""))

        if st == "connect":
            r.state = scan_connect(self.target, port, self.timeout)

        elif st == "syn" and self._dispatcher:
            state, ttl = scan_syn(self.target, port, self.src_ip,
                                  self.timeout, self._dispatcher)
            r.state = state
            if ttl and not self.ttl_sample:
                self.ttl_sample = ttl

        elif st in ("xmas", "null", "fin") and self._dispatcher:
            flags = self.FLAG_MAP[st]
            r.state = scan_stealth(self.target, port, flags, self.src_ip,
                                   self.timeout, self._dispatcher)

        elif st == "udp":
            r.state = scan_udp(self.target, port, self.src_ip, self.timeout)

        else:
            r.state = scan_connect(self.target, port, self.timeout)

        # Banner grab only for open TCP ports
        if r.state == "open" and proto == "tcp" and self.service_detect:
            r.version = grab_banner(self.target, port, timeout=2.0)

        return r


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

def print_banner_art():
    art = """\
 ██████╗ ██╗   ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
 ██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██████╔╝ ╚████╔╝ ███████╗██║     ███████║██╔██╗ ██║
 ██╔═══╝   ╚██╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
 ██║        ██║   ███████║╚██████╗██║  ██║██║ ╚████║
 ╚═╝        ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝"""
    console.print(Align.center(Text(art, style="bright_green")))
    console.print(Align.center(Text(
        "Python Network Scanner  •  raw sockets from scratch",
        style="dim green")))
    console.print(Align.center(Text("─" * 56, style="bright_black")))

    parts = [
        Text("● ROOT", style="bold green") if is_root()
        else Text("● USER (some scans require root)", style="bold yellow")
    ]
    console.print(Align.center(Columns(parts)))
    console.print()


def state_text(state: str) -> Text:
    colors = {
        "open":         ("● open",         "bold bright_green"),
        "closed":       ("✕ closed",        "dim red"),
        "filtered":     ("◌ filtered",      "yellow"),
        "open|filtered":("◑ open|filtered", "yellow"),
    }
    label, style = colors.get(state, (state, "white"))
    return Text(label, style=style)


def print_results(scanner: Scanner, elapsed: float):
    results = scanner.results
    open_ports   = [r for r in results if r.state == "open"]
    filtered     = [r for r in results if "filtered" in r.state]
    closed_count = sum(1 for r in results if r.state == "closed")

    console.print()
    console.print(Rule("[bold bright_green] Scan Complete [/]",
                       style="bright_green"))
    console.print()

    # ── Summary panel ────────────────────────────────────────────────────
    summary = Table(box=box.SIMPLE, show_header=False,
                    padding=(0, 2), show_edge=False)
    summary.add_column(style="dim green")
    summary.add_column(style="bright_white")
    summary.add_row("Target",   scanner.target)
    summary.add_row("Scan type", scanner.scan_type.upper())
    summary.add_row("Source IP", scanner.src_ip)
    summary.add_row("Ports scanned", str(len(scanner.ports)))
    summary.add_row("Duration",  f"{elapsed:.2f}s")
    if scanner.os_guess:
        summary.add_row("OS guess (TTL)",
                        f"{scanner.os_guess}  (TTL ≈ {scanner.ttl_sample})")
    summary.add_row("Open", str(len(open_ports)))
    summary.add_row("Filtered", str(len(filtered)))
    summary.add_row("Closed", str(closed_count))
    console.print(Panel(summary,
                        title="[bold bright_green]Summary[/]",
                        border_style="bright_green"))
    console.print()

    # ── Open ports ───────────────────────────────────────────────────────
    if open_ports:
        t = Table(box=box.SIMPLE_HEAD, border_style="green",
                  header_style="bold bright_green",
                  show_edge=False, padding=(0, 1))
        t.add_column("PORT",    style="bold bright_green", width=10)
        t.add_column("PROTO",   style="dim green",         width=6)
        t.add_column("STATE",                              width=14)
        t.add_column("SERVICE", style="cyan",              width=16)
        t.add_column("VERSION", style="bright_white")
        for r in open_ports:
            t.add_row(
                str(r.port),
                r.protocol,
                state_text("open"),
                r.service or "unknown",
                r.version or "",
            )
        console.print(Panel(
            t,
            title=f"[bold bright_green]Open Ports  ({len(open_ports)})[/]",
            border_style="bright_green"))
        console.print()

    # ── Filtered ports ───────────────────────────────────────────────────
    if filtered:
        n = len(filtered)
        if n <= 15:
            t2 = Table(box=box.SIMPLE_HEAD, border_style="yellow",
                       header_style="bold yellow",
                       show_edge=False, padding=(0, 1))
            t2.add_column("PORT",    style="yellow",    width=10)
            t2.add_column("PROTO",   style="dim green", width=6)
            t2.add_column("STATE",                      width=18)
            t2.add_column("SERVICE", style="dim white")
            for r in filtered:
                t2.add_row(str(r.port), r.protocol,
                           state_text(r.state),
                           r.service or "")
            console.print(Panel(t2,
                                title=f"[yellow]Filtered Ports  ({n})[/]",
                                border_style="yellow"))
        else:
            console.print(Panel(
                Text(f"{n} filtered ports  "
                     "(use -v to list all in saved output)",
                     style="yellow"),
                title=f"[yellow]Filtered Ports  ({n})[/]",
                border_style="yellow"))
        console.print()

    if not open_ports and not filtered:
        console.print(Panel(
            Text("No open or filtered ports found.", style="dim"),
            border_style="bright_black"))
        console.print()


# ─────────────────────────────────────────────────────────────────────────────
# PERSISTENCE
# ─────────────────────────────────────────────────────────────────────────────

def save_results(scanner: Scanner, elapsed: float, cmd: list[str]) -> tuple[Path, Path]:
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = safe_filename(scanner.target).replace(".", "_")
    base = str(OUTPUT_DIR / f"{ts}_{safe}_{scanner.scan_type}")

    # ── Text ─────────────────────────────────────────────────────────────
    txt_path = Path(base + ".txt")
    with open(txt_path, "w") as f:
        f.write(f"# pyscan results\n")
        f.write(f"# Target   : {scanner.target}\n")
        f.write(f"# Scan type: {scanner.scan_type}\n")
        f.write(f"# Command  : {' '.join(cmd)}\n")
        f.write(f"# Date     : {datetime.datetime.now().isoformat()}\n")
        f.write(f"# Duration : {elapsed:.2f}s\n")
        if scanner.os_guess:
            f.write(f"# OS guess : {scanner.os_guess} (TTL ~{scanner.ttl_sample})\n")
        f.write("\n")
        f.write(f"{'PORT':<10} {'PROTO':<6} {'STATE':<16} {'SERVICE':<18} VERSION\n")
        f.write("-" * 70 + "\n")
        for r in scanner.results:
            if r.state not in ("closed",):
                f.write(f"{r.port:<10} {r.protocol:<6} {r.state:<16} "
                        f"{r.service:<18} {r.version}\n")

    # ── JSON ─────────────────────────────────────────────────────────────
    json_path = Path(base + ".json")
    data = {
        "target": scanner.target,
        "scan_type": scanner.scan_type,
        "command": cmd,
        "timestamp": datetime.datetime.now().isoformat(),
        "elapsed_seconds": round(elapsed, 3),
        "os_guess": scanner.os_guess,
        "ttl": scanner.ttl_sample,
        "ports": [
            {
                "port": r.port,
                "protocol": r.protocol,
                "state": r.state,
                "service": r.service,
                "version": r.version,
            }
            for r in scanner.results
        ],
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    return txt_path, json_path


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pyscan",
        description="Python Network Scanner — Nmap-like scanning from scratch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scan types:
  connect  Full TCP connect (no root)         [default]
  syn      SYN stealth half-open (root)
  xmas     FIN+PSH+URG flags     (root)
  null     No TCP flags          (root)
  fin      FIN flag only         (root)
  udp      UDP with ICMP detect  (root)

Timing:
  T0  Paranoid (1 worker,  5.0s timeout)
  T1  Sneaky   (3 workers, 3.0s timeout)
  T2  Polite   (10 workers,2.0s timeout)
  T3  Normal   (20 workers,1.0s timeout)   [default]
  T4  Aggressive (50,      0.5s)
  T5  Insane   (100 workers,0.3s timeout)

Examples:
  python3 pyscan.py 192.168.1.1
  python3 pyscan.py 192.168.1.1 -sS -sV -T4
  python3 pyscan.py 192.168.1.1 -p 22,80,443 -sV
  python3 pyscan.py 192.168.1.1 --top-ports 100 -O
  sudo python3 pyscan.py 192.168.1.1 -sS -O -sV -T4 -o results
  python3 pyscan.py 192.168.1.0/24 -Pn --top-ports 20
        """,
    )
    p.add_argument("target",
                   help="Target IP, hostname, or CIDR (e.g. 192.168.1.0/24)")
    p.add_argument("-p", "--ports", default="1-1024",
                   help="Port spec: 22,80,443 | 1-1000 | - (all). Default: 1-1024")
    p.add_argument("--top-ports", type=int, metavar="N",
                   help="Scan top N most common ports (overrides -p)")

    # Scan type flags (mutually exclusive, nmap-style)
    stype = p.add_mutually_exclusive_group()
    stype.add_argument("-sT", "--connect",  dest="scan", action="store_const",
                       const="connect", help="TCP Connect scan (default, no root)")
    stype.add_argument("-sS", "--syn",      dest="scan", action="store_const",
                       const="syn",     help="SYN stealth scan (root)")
    stype.add_argument("-sX", "--xmas",     dest="scan", action="store_const",
                       const="xmas",    help="Xmas scan (root)")
    stype.add_argument("-sN", "--null",     dest="scan", action="store_const",
                       const="null",    help="NULL scan (root)")
    stype.add_argument("-sF", "--fin",      dest="scan", action="store_const",
                       const="fin",     help="FIN scan (root)")
    stype.add_argument("-sU", "--udp",      dest="scan", action="store_const",
                       const="udp",     help="UDP scan (root for ICMP detection)")
    p.set_defaults(scan="connect")

    p.add_argument("-sV", "--service-detect", action="store_true",
                   help="Grab service banners (version detection)")
    p.add_argument("-O",  "--os-detect",      action="store_true",
                   help="OS fingerprinting via TTL analysis")
    p.add_argument("-A",  "--aggressive",     action="store_true",
                   help="Shorthand for -sV -O (aggressive mode)")
    p.add_argument("-T",  "--timing", default="T3",
                   choices=list(TIMING.keys()),
                   help="Timing template T0–T5 (default: T3)")
    p.add_argument("-Pn", "--no-ping", action="store_true",
                   help="Skip host discovery (assume host is up)")
    p.add_argument("-o",  "--output", metavar="STEM",
                   help="Save results: <STEM>.txt and <STEM>.json")
    p.add_argument("-v",  "--verbose", action="store_true",
                   help="Show all ports including closed ones in output")
    return p


def main():
    parser = build_parser()
    args   = parser.parse_args()

    print_banner_art()

    # Aggressive mode
    if args.aggressive:
        args.service_detect = True
        args.os_detect = True

    # Resolve port list
    ports = parse_ports(args.ports, top=args.top_ports or 0)

    # Resolve targets (supports CIDR)
    targets = parse_targets(args.target)
    if not targets:
        console.print("[red]No valid targets found.[/]")
        sys.exit(1)

    cmd = sys.argv[:]

    for target_ip in targets:
        console.print(Panel(
            f"[bright_green]Target:[/]  {target_ip}\n"
            f"[bright_green]Ports :[/]  {len(ports)} port(s)  "
            f"({ports[0]}–{ports[-1]} range)\n"
            f"[bright_green]Scan  :[/]  {args.scan.upper()}  "
            f"({TIMING[args.timing]['label']} timing — "
            f"{TIMING[args.timing]['workers']} workers, "
            f"{TIMING[args.timing]['timeout']}s timeout)",
            title="[bold bright_green]pyscan[/]",
            border_style="bright_green"))

        scanner = Scanner(
            target_ip=target_ip,
            ports=ports,
            scan_type=args.scan,
            timing=args.timing,
            service_detect=args.service_detect or args.aggressive,
            os_detect=args.os_detect or args.aggressive,
            no_ping=args.no_ping,
            verbose=args.verbose,
        )

        start = time.time()
        results = scanner.run()
        elapsed = time.time() - start

        if not scanner.host_up and not args.no_ping:
            console.print(Panel(
                f"[yellow]Host {target_ip} appears down. "
                f"Use -Pn to skip discovery and scan anyway.[/]",
                border_style="yellow"))
            continue

        print_results(scanner, elapsed)

        # Save output
        if args.output or True:  # always save
            txt, js = save_results(scanner, elapsed, cmd)
            console.print(Panel(
                Text(f"📄  {txt}\n📊  {js}", style="cyan"),
                title="[bold bright_green]Results Saved[/]",
                border_style="bright_green"))

    # Clean up raw socket dispatcher
    global _dispatcher
    if _dispatcher:
        _dispatcher.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim green]Interrupted. Exiting.[/]\n")
        sys.exit(0)
