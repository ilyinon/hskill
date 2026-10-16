---
name: reverse-shell-techniques
description: >-
  Reverse shell techniques playbook. Use when establishing remote shells including language one-liners, encrypted shells (OpenSSL/socat/ncat), web shells, PTY upgrades, file transfer methods, PowerShell shells, and Windows payload generation.
---

# Reverse Shell Techniques

## Working approach

- Establish that command execution and the requested connection are authorized
- Record platform, egress, listener direction, transport, and terminal needs
- Choose a compatible existing recipe and verify destination identity and cleanup.

## Evidence and limits

The intended controlled endpoint receives the expected session under the documented network and privilege constraints.

A listener hit is not proof of the expected host or identity; a shell is not required when a smaller proof already satisfies the user's goal, and persistence needs separate authorization.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. REVERSE vs BIND SHELL DECISION; 2. ENCRYPTED SHELLS; 3. WEB SHELLS; 4. PTY UPGRADE SEQUENCE; 5. FILE TRANSFER METHODS | [Read](./references/01-reverse-vs-bind-shell-decision.md) |
| 6. POWERSHELL REVERSE SHELLS; 7. MSFVENOM PAYLOADS; 8. DECISION TREE | [Read](./references/02-powershell-reverse-shells.md) |
| Advanced: REVERSE SHELL CHEATSHEET | [Read](./SHELL_CHEATSHEET.md) |
