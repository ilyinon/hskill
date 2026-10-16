---
name: linux-privilege-escalation
description: >-
  Linux privilege escalation playbook. Use when you have low-privilege shell access and need to escalate to root via SUID/SGID binaries, capabilities, cron abuse, kernel exploits, misconfigurations, or credential harvesting on Linux systems.
---

# Linux Privilege Escalation

## Working approach

- Record current UID/groups, capabilities, sudo policy, service/task paths, mounts, kernel, and security controls
- Identify a writable or delegated resource used by a more privileged principal
- Test the smallest reversible permission effect.

## Evidence and limits

The local principal crosses the intended privilege boundary through a reproducible effective configuration or vulnerability.

SUID, a named capability, root in a container, or a writable file alone is not sufficient; execution context and actual privileged use must be established.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ENUMERATION CHECKLIST; 2. SUID/SGID EXPLOITATION; 3. CAPABILITIES ABUSE; 4. CRON / TIMER ABUSE | [Read](./references/01-enumeration-checklist.md) |
| 5. NFS NO_ROOT_SQUASH; 6. WRITABLE /etc/passwd OR /etc/shadow; 7. LD_PRELOAD / LD_LIBRARY_PATH WITH SUDO; 8. DOCKER GROUP → ROOT; 9. PYTHON / PERL / RUBY LIBRARY HIJACKING; 10. AUTOMATED TOOLS; 11. PRIVILEGE ESCALATION DECISION TREE | [Read](./references/02-nfs-no-root-squash.md) |
| Advanced: Kernel Exploits Checklist | [Read](./KERNEL_EXPLOITS_CHECKLIST.md) |
| Advanced: SUID/SGID & Capabilities Exploitation Tricks | [Read](./SUID_CAPABILITIES_TRICKS.md) |
