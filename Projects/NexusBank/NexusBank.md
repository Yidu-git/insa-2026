---
tags:
---
# Project over view
## Description
**NexusBank** is a project that aims to combat sim swapping attacks and other malicious attacks that target banks.

## Tech stack
The frontend is built with React JS with tailwindcss.

The backend is built with SQLite (temporary) with future plans to replace MongoDB or PostgreSQL, with Redis. `bycript` for encryption and hashing.

## Features
- Near-Pay
	- Requests
- Full transaction history
- Security keys (Temporary and Transfer keys)
- Loans
	- Monthly loan payments
	- Autonomous payments
- Link Requests
- Payment links
- Device linking
	- Linked device training
- Temporary account transfer window
## Test/Development features
- **`seed.js`**, a script that creates default accounts to test features with
- **`utils.js`**, a script with function modules to use throughout the app, example; conversion, testing, etc...