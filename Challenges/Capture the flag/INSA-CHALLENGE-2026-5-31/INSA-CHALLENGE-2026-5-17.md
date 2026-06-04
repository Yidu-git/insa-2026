---
cssclasses:
  - jbm-note
Date: 2026-05-31
---

# Mobile security Challenge

| **Target** :LiTarget:              | *Mobile application* |
| ---------------------------------- | -------------------- |
| Date :LiCalendar:                  | 31/5/2026            |
| Main attack type                   | ...                  |
| Secondary attack type              | ...                  |
| Tools :LiToolCase: :               | JADX, GenY Motion    |
| Criticality :RiAlarmWarningLine: : | **...**              |

---
# **RESULTS**
---
## Flags found
1. First flag - Login
	- *F1ag_0n3*
2. Second flag - Exported activities
	- *S3c0nd_F1ag*
3. Third flag - Resources
	- *F1ag_thr33*
4. Fourth flag -  Login 2
	- *4_overdone_omelets*
5. Fifth flag - Exported broadcast receiver
	- *{F1v3!}*
6. Sixth flag - Login 3
	- *{This_Isn't_Where_I_Parked_My_Car}*
7. Seventh flag
	- *S3V3N_11*
	- *hunter2*
8. Eighth flag
	- *C10ud_S3cur1ty_lol*
9. Ninth flag
	- *W25pbmUhX2ZsYWdd*
10. Tenth flag
	- *...*
11. Eleventh flag
	- *...*
12. Twelfth flag
	- *...*
13. Thirteenth flag
	- *...*
14. Fourteenth flag
	- *...*
15. Fifteenth flag
	- *...*
16. Sixteenth flag
	- *...*
17. Seventeenth flag
	- *...*
18. Eighteenth flag
	- *...*
---
# Preparation
---
## Tools
1. **JADX**
	- On :SiKalilinux: *Kali Linux*
2. **Android studio AVD** (ROOTED)
	- Android 11 (API 30)

---
# Initial investigation/enumeration
---
## **Enumeration**
### Looking through the app
The app is a simple CTF with 18 flags, it includes a flag overview and and `XSSTEXT` section that reflects text inserted into the input field. This section is not used to find other flags, as stated by the text : `Fun no flag vulnerable XSS field to test payloads.`

## **Vulnerability scanning**
...

---
# Exploiting and  Investigation
---
## First flag
The *`FLAG ONE - LOGIN`* section contains a single input field, this can likely be exploited through checking the source code.

Checking the source code with JADX-GUI reveals the first flag as a string. It is located in `First_Flag_Activity`. Inserting the flag into the input field on the app confirms the flag.

## Second flag
The *`FLAG TWO - EXPORTED ACTIVITY`* section contains the text : 
*There is a way to bypass the main activity and invoke other activities that are exported.*.

This hints at a vulnerability that can be exploited through **`adb`**. Checking the `AndroidManifest.xml`, there is an activity called b25lActivity with **exported** set to **true**. Running the activity with ADB shell shows the second flag.

```powershell
./adb shell am start -n b3nac.injuredandroid/b3nac.injuredandroid.b25lActivity
```

## Third flag
The third flag is similar to the first, the flag is contained in a static string with the name `cmVzb3VyY2VzX3lv`. Checking the `string.xml` file reveals the string it leads to, which contains the third flag.

## Fourth flag
The forth flag can be found after investigating the activity, which also contains an input. This time the flag is encoded in Base64 in `g.java` or the `g` file.

## Fifth flag
The fifth flag can be found by opening and closing the page repeatedly. It is intended to work by sending a broadcast repeatedly. It can also be found by inspecting the receiver, the flag is base64 encoded and encrypted however.

Calling the function after restarting the app works:
```PowerShell
./adb shell am broadcast -a com.b3nac.injuredandroid.intent.action.CUSTOM_INTENT -n b3nac.injuredandroid/.FlagFiveReceiver
```

## Sixth flag
Flag six is another page with an input, the activity compares input with a base64 encoded and encrypted string : `k3FElEG9lnoWbOateGhj5pX6QsXRNJKh///8Jxi8KXW7iDpk2xRxhQ==`. 

The string is decoded with class `k.a()`, this is the same class that is used to decode the forth flag, Further exploration through the class, we can find two important classes.

The `k.a` uses DES encryption with a passkey that is encoded in base64. The key is located in `h.a` as a base64 encoded string. `h.b` can be found with `h.a`.

Decoded strings:
**.a** :
`Q2FwdHVyM1RoMXM=`
*Base64 Decoded* : `Captur3Th1s`
**.b** :
`e0NhcHR1cjNUaDFzVG9vfQ==`
*Base64 Decoded* : `{Captur3Th1sToo}`

Using [Cyber Chef](gchq.github.io/CyberChef/), decrypting it using the following blocks gave the output  **`{This_Isn't_Where_I_Parked_My_Car}`** :
1. From Base64
2. DES Decrypt
	1. Encryption key : `Captur3T` (Since the key is 8 bytes long)
	2. Encryption key format : UTF8
	3. Mode : ECB

## Seventh flag
The seventh flag page is a login form with a flag input and a password input. Inspecting the activity file reveals base64 encoded strings :

`VGhlIGZsYWcgaGFzaCE=` -> **`The flag hash!`**
`MmFiOTYzOTBjN2RiZTM0MzlkZTc0ZDBjOWIwYjE3Njc=` -> ***`2ab96390c7dbe3439de74d0c9b0b1767`*** -> MD5 Crack : **`hunter2`**
`VGhlIGZsYWcgaXMgYWxzbyBhIHBhc3N3b3JkIQ==` -> **`The flag is also a password!`**

The second string contains an MD5 hash which contains the password. The flag is hidden in the string found from the previous flag. It is encrypted with **ROT47**. Decrypting it gives us a URL, calling it gives us the flag `S3V3N_11`.

`9EEADi^^:?;FC652?5C@:5]7:C632D6:@]4@>^DB=:E6];D@?` -> **`https://injuredandroid.firebaseio.com/sqlite.json`**

```json
"S3V3N_11"
```

## Eighth flag



## Ninth flag
The ninth flag activity file contains a base64 encoded string which leads to an endpoint:
`ZmxhZ3Mv` -> **`flags/`**

Using the `.json` trick from the hint gives us the flag.
`https://injuredandroid.firebaseio.com/flags.json`
```json
"[nine!_flag]"
```

Inserting the flag doesn't work, further inspection of the activity reveals that the string is base64 decoded after insertion. As such encoding the string works.
`[nine!_flag]` -> **``W25pbmUhX2ZsYWdd``**

## Tenth flag
