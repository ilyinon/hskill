---
name: sandbox-escape-techniques
description: >-
  Sandbox escape playbook. Use when breaking out of Python sandbox, Lua sandbox, seccomp filter, chroot jail, container/Docker, browser sandbox, or namespace isolation to achieve unrestricted code execution or file access.
---

# Sandbox Escape Techniques

## Working approach

- Identify whether the boundary is a language evaluator, restricted shell, chroot, namespace, browser, or application sandbox
- Record available objects/syscalls/privileges and denied operations
- Validate one boundary transition in a disposable local reproduction.

## Evidence and limits

A permitted test accesses a capability outside the stated sandbox policy.

Code execution inside the sandbox is not automatically escape; chroot, namespaces, seccomp, language restrictions, and browser process boundaries are distinct.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SANDBOX TYPE IDENTIFICATION; 2. PYTHON SANDBOX ESCAPE (OVERVIEW); 3. LUA SANDBOX ESCAPE; 4. CHROOT ESCAPE; 5. BROWSER SANDBOX ESCAPE (OVERVIEW); 6. NAMESPACE ESCAPE | [Read](./references/01-sandbox-type-identification.md) |
| 7. RBASH / RESTRICTED SHELL ESCAPE; 8. DECISION TREE | [Read](./references/02-rbash-restricted-shell-escape.md) |
| Advanced: Python Sandbox Escape (Pyjail) — Complete Methodology | [Read](./PYTHON_SANDBOX_ESCAPE.md) |
| Advanced: Seccomp Bypass — Architecture Confusion, io_uring, Allowed Syscall Chaining | [Read](./SECCOMP_BYPASS.md) |
