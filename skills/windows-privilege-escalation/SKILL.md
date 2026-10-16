---
name: windows-privilege-escalation
description: >-
  Windows local privilege escalation playbook. Use when you have low-privilege shell access on Windows and need to escalate via token abuse, Potato exploits, service misconfigurations, DLL hijacking, UAC bypass, or registry autoruns.
---

# Windows Privilege Escalation

## Working approach

- Identify effective token privileges, integrity, OS/build, service/task/registry ACLs, and writable paths
- Select a reachable permission path whose prerequisite exists
- Verify a minimal local boundary change and restore owned test artifacts.

## Evidence and limits

The starting principal gains a capability outside its intended token/ACL boundary through the demonstrated path.

A privilege name, writable location, or Potato-family compatibility row alone is insufficient; UAC elevation for an existing administrator differs from standard-user-to-admin escalation.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ENUMERATION CHECKLIST; 2. TOKEN MANIPULATION & POTATO EXPLOITS; 3. SERVICE MISCONFIGURATIONS; 4. DLL HIJACKING; 5. ALWAYSINSTALLELEVATED | [Read](./references/01-enumeration-checklist.md) |
| 6. SCHEDULED TASK ABUSE; 7. REGISTRY AUTORUNS; 8. NAMED PIPE IMPERSONATION; 9. AUTOMATED TOOLS; 10. PRIVILEGE ESCALATION DECISION TREE | [Read](./references/02-scheduled-task-abuse.md) |
| Advanced: Token Manipulation & Potato Family Detailed Comparison | [Read](./TOKEN_POTATO_TRICKS.md) |
| Advanced: UAC Bypass Techniques Matrix | [Read](./UAC_BYPASS_METHODS.md) |
