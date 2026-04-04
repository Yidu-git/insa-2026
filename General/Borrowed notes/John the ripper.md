Here is the step-by-step process to "crack" a password using JTR.

---

## 1. The "Golden Rule" of John the Ripper

John the Ripper doesn’t usually point directly at a file like `secret.zip`. Instead, it needs a **hash**. You first have to "extract" the password's fingerprint into a format John understands.

## 2. Preparing the Target

If you are practicing, you likely have one of two scenarios:

### Scenario A: Cracking a ZIP or PDF

If you created a file and want to crack it, you use a "to-john" tool.

1. **Extract the hash:** `zip2john yourfile.zip > hash.txt`
    
2. **Crack it:** `john hash.txt`
    



---

## 3. Choosing Your Attack Mode

John is smart, but you can make it faster by telling it _how_ to guess.

| Mode             | Command                                                     | Description                                                        |
| ---------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| **Single Crack** | `john --single hash.txt`                                    | Uses the username as the password (surprisingly effective).        |
| **Wordlist**     | `john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt` | The "standard" way. It tries every word in a list.                 |
| **Incremental**  | `john --incremental hash.txt`                               | Brute force. Tries every possible combination (takes the longest). |

Export to Sheets

---

## 4. Viewing the Results

Once John finds the password, it might happen so fast you miss it, or you might want to check it later. John saves everything in a "pot" file.

- **To see the cracked password:** `john --show hash.txt`
    

> [!IMPORTANT] **A Note on "Rockyou":** On a fresh Kali install, the famous `rockyou.txt` wordlist is compressed. Before using it, you need to run: `gunzip /usr/share/wordlists/rockyou.txt.gz`

---

## 5. Summary Workflow

1. **Get the hash** using the appropriate tool (`zip2john`, `pdf2john`, `unshadow`).
    
2. **Point John** at that hash file.
    
3. **Specify a wordlist** if you want speed.
    
4. **Show results** once the process finishes.

# step by step instructions 
### 1. Create a "Secret" File

First, let's create a simple text file that contains some data you want to protect.

Bash

```
echo "This is my top secret data!" > practice.txt
```

### 2. Lock the File with a Password

Now, we will compress this into a password-protected ZIP file.

- **-e**: Stands for "encrypt."
    
- **practice.zip**: This is the name of the new locked file.
    
- **practice.txt**: This is the file we are putting inside.
    

Run this command:

Bash

```
zip -e practice.zip practice.txt
```

**Important:** When prompted, enter a **10-digit number** (e.g., `1234567890`) so we can test the numeric mask we discussed earlier. You won't see the numbers as you type them.

### 3. Verify it is Locked

Try to peek inside the file without the password.

Bash

```
unzip -p practice.zip
```

It should ask you for a password. If you just hit enter, it should say "incorrect password" or "skipping."

---

### 4. Extract the Hash (The First Step of Cracking)

Now we move into the "John the Ripper" workflow. We need to turn that ZIP file into a text format that John can read.

Bash

```
zip2john practice.zip > practice.hash
```

### 5. View the Hash

If you want to see what a "password fingerprint" looks like, run:

Bash

```
cat practice.hash
```

You’ll see a long string of characters starting with `$zip2$`. This is what John will actually be attacking.
### 6. The Execution

Run this command in your terminal:

Bash

```
john --mask=?d?d?d?d?d?d?d?d?d?d noah.hash
```

### 7. While it’s running (Don't just wait!)

John is a "silent" worker, but you can interact with it while it runs. Try these keys:

- **Spacebar or Enter:** Shows the status (how many guesses made, percentage done, and the ETA).
    
- **'q':** Quits the session (don't worry, John saves your progress automatically).
    
- **'s':** Shows the current "cracked" count if you are running multiple files.
    

---

### 8. What to expect

A 10-digit space has **10,000,000,000 (10 billion)** possible combinations.

- **If the password is "0000000001":** It will finish in seconds.
    
- **If the password starts with "999...":** It might take a while depending on your CPU speed.
    

### 9. Viewing the Result

Once John finds it, the terminal will scream **"Session completed"** and display the password in plain text. If you missed it because the text scrolled too fast, just run:

Bash

```
john --show practice.hash
```

