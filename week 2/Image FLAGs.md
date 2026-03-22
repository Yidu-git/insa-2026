Image: [challenge.jpg](challenge.jpg)![[challenge.jpg]]
## Flags 1 & 2
The `strings` command in Linux is used to extract printable character sequences (text strings) from binary files and other non-text files. We can use this command to check metadata and any embedded strings. Using grep to sort through the text we can find the first two flags.
```shell
 strings challenge.jpg |  grep -oE 'FLAG{[a-zA-Z0-9_]+}' | sort -u
```
output:
```
FLAG{ALWAYS_Check_Metadata}
FLAG{Strings_leak_information}
```
Note that flag one can be checked through 
## Flag 3
To find the forth flag we can use **`bitwalk`** which is 
Checking for hidden files with `bitwalk`:
```Shell
binwalk challenge.jpg
binwalk -e challenge.jpg
```
This is the forth flag, there is an embedded file `flag4.txt` that contains *base64* double encoded text that confirms this.
```shell
echo "Umt4QlIzdGhjSEJsYm1SbFpGOTZhWEI5Q2c9PQo=" | base64 -d
echo "RkxBR3thcHBlbmRlZF96aXB9Cg==" | base64 -d
```
Output: **`FLAG{appended_zip}`**
## Flag 4
Through brute forcing with the default `rockyou.txt` provided in Kali Linux and the **`stegseek`** tool, the password can be brute forced.
```shell
steghide extract -sf challenge.jpg -wl rockyou.txt
```

The password found is "password123" and the extracted file is "flag5.txt" that is stored in `challenge.jpg.out` which contains `FLAG{steghide_protected}`.
## Flag 5
