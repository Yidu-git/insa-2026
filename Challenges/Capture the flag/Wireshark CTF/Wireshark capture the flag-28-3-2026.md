# Flags
A folder contains 5 capture files (`challenge_1_traffic.pcap,...challenge_5_traffic.pcap`) with flags in each, a hints file is given with hints for each challenge.
`hints`:
```
Challenge 1: 
Hint: “Sometimes secrets travel unencrypted. Inspect the messages your browser asks for.”

Challenge 2:
Hint: “Even small questions can carry hidden messages. Check what your system is asking the internet.”

Challenge 3:
Hint: “The answer might be broken into pieces across multiple packets. Reassemble to see the whole picture.”

Challenge 4:
Hint: “Some messages arrive encoded. The transport might reveal patterns in the body rather than the headers.”

Challenge 5:
Hint: “Even simple pings can carry secrets inside them. Don’t just look at the summary—peek at the payload.”
```

---
# Flag 1

![[Wireshark-CTF-screenshot-1.png]]

Flag 1 contains a simple flag (`FLAG{http_easy_capture}`), this flag shows up when filtering through the packets captured with `http`.

---
# Flag 2
by using the filter `ip.src == 192.168.0.115 && frame contains "FLAG"` we get the flag `FLAG_dns_exfiltration_.example.com`
# Flag 3
Using the filter `tcp && ip.src == 127.0.0.1` this time, we can follow the **`tcp`** stream to get the third flag:
```
Hello,
Here is your secret flag:
FLAG{tcp_stream_reassembly}
Thank you!
```
![[Wireshark-CTF-screenshot-2.png]]
# Flag 4
By filtering through the IP `127.0.0.1` again but with **SMTP** instead of *TCP*, we can find and follow the stream to get the base64 encoded string : `RkxBR3tzbXRwX2Jhc2U2NH0=`, which can be decoded to give: `FLAG{smtp_base64}`
We can get this using the command ```
```bash
echo "RkxBR3tzbXRwX2Jhc2U2NH0=" | base64 -d
```
![[Wireshark-CTF-screenshot-4.png]]
# Flag 5
Using the standard ping protocol **`icmp`**, we can find the flag `FLAG{ic_icmp}`
![[Wireshark-CTF-screenshot-5.png]]