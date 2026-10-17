---
name: linux-security-bypass
description: >-
  Linux security mechanism bypass playbook. Use when facing restricted bash/rbash, read-only or noexec filesystems, AppArmor, SELinux, seccomp filters, or audit logging that must be evaded during post-exploitation.
---

# Linux Security Bypass

## Working approach

- Identify the actual restricting control and namespace/runtime context
- Compare the denied operation with a controlled permitted alternative
- Verify the specific filesystem, syscall, policy, or shell boundary rather than inferring unrestricted access.

## Evidence and limits

The tested action bypasses the identified control under the documented policy and privileges.

One bypass does not disable every control; preserve engagement evidence and do not use log deletion or audit shutdown as a default validation step.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. RESTRICTED BASH (rbash) BYPASS; 2. READ-ONLY / NOEXEC FILESYSTEM EXECUTION; 3. APPARMOR BYPASS | [Read](./references/01-restricted-bash-rbash-bypass.md) |
| 4. SELINUX BYPASS; 5. SECCOMP BYPASS; 6. AUDIT EVASION — EVIDENCE-ALTERING LAB EXAMPLES; 7. LINUX SECURITY BYPASS DECISION TREE | [Read](./references/02-selinux-bypass.md) |
