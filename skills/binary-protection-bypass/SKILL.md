---
name: binary-protection-bypass
description: >-
  Binary protection bypass playbook. Use when identifying and bypassing ASLR, PIE, NX/DEP, stack canary, RELRO, FORTIFY_SOURCE, CET, and MTE protections in ELF binaries to enable exploitation.
---

# Binary Protection Bypass

## Working approach

- Inspect the actual binary, loader, architecture, and enabled mitigations
- Match the available read/write/control-flow primitive to those protections
- Validate the chosen path against the exact runtime and memory layout.

## Evidence and limits

A local reproducible chain demonstrates the claimed mitigation boundary and intended control.

A checksec label or historical version table is not a bypass; CET, allocator changes, pointer authentication/tagging, and runtime configuration alter feasibility.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. PROTECTION IDENTIFICATION; 2. ASLR BYPASS; 3. PIE BYPASS; 4. NX / DEP BYPASS; 5. RELRO BYPASS | [Read](./references/01-protection-identification.md) |
| 6. CANARY BYPASS; 7. FORTIFY_SOURCE BYPASS; 8. CET (Control-flow Enforcement Technology); 9. MTE (Memory Tagging Extension, ARM); 10. DECISION TREE | [Read](./references/02-canary-bypass.md) |
| Advanced: Protection Bypass Matrix — Comprehensive Cross-Reference | [Read](./PROTECTION_BYPASS_MATRIX.md) |
