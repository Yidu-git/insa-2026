#### 1) The full reset
 `sudo chmod 640 <file>`
 
#### 2) The executioner
 `sudo chmod 755 <file>`
 
#### 3) The secure log
`sudo chmod 664 <file>`

#### 4) Binary to octal
`sudo chmod 640 <file>`

#### 5) The mystery code
No

#### 6) File creation
```shell
touch Audit.txt
sudo chmod 750 Audit.txt
```

#### 7) Numeric to symbolic
$$741 = 111,110,001 => rwx,rw-,--x$$
`-rwxrw---x`

#### 8) Numeric to symbolic
$$500 = 101,000,000 => r-x,r--,---$$
`-r-x------`

#### 9) Symbolic to numeric
$$r-x,rw-,r-- => 101,110,100 = 564$$
`-r-xrw-r--`