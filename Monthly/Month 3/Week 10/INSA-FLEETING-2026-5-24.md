---
cssclasses:
  - jbm-note
---
# Reverse Engineering 2
## Workflow
### Recon
Finding out the file properties like file size, metadata and architecture.
### Static analysis
Analyzing strings, imports, and disassembly. This is usually done using tools like `Ghidra`.
### Dynamic analysis
Running the software in sandboxes with set breakpoints(functions where the software to stop running when it hits). This is usually done using tools like `x64dbg` and `binaryninja`.
### Identify logic
Identifying and mapping the software logic and function.
### Document
Creating notes on findings, addresses, function names, IOCs and behavior.
### Reporting
Write a report or patch the binary for your goal.

## Tools
- `IDA Pro`
- `x64dbg`
- `Radare2`
- `DIE`
- `Ghidra`
- `Ollydbg`
- `BinaryNinja`
- `PE-bear`

# Bypassing password authentication
Analyzing most software made with the x86 architecture, Most checks can be bypassed by changing `je` to `jne` or vice versa.