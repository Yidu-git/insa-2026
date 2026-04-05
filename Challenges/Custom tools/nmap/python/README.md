# Intro
This Python script mimics `nnmap`. This script is helpful for people with python experience that want to analyze how nmap works without looking through the complex source code. While this script doesn't include all features of `nmap` it can has all the main features.

# How it works
## Running the script
Running the script is very similar to running `nmap` with the difference being that instead of runnign it as a root command, it must be run with python. While this is the case, due to the `argparse` python library it supports flags.

Example:
Scanning on the ip "192.168.1.10"
```Bash
python pyscan.py -Pn -sS 192.168.1.10
```

The advantage of this script is the provided CLI for a progress bar and other important information such as open ports and elapsed time.

## Results
After running a command, a folder called *pyscan_results* will be created which contains two files in plain text and json format named by the date, time and ip address scanned. An example folder is provided.

# Disclaimer
This project was generated with **Claude Code**. Human-written documentation will be added.
