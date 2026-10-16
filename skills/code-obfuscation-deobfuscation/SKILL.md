---
name: code-obfuscation-deobfuscation
description: >-
  Code obfuscation analysis and deobfuscation playbook. Use when reversing
  binaries protected by junk code, opaque predicates, self-modifying code,
  control flow flattening, VM protection, or string encryption.
---

# Code Obfuscation Deobfuscation

## Working approach

- Identify the protection layer and the input/output behavior to preserve
- Separate strings/imports, opaque predicates, flattened control flow, self-modification, and VM dispatch
- Simplify one layer and compare traces or outputs.

## Evidence and limits

The simplified representation explains reachable behavior and agrees with the original on relevant test inputs.

Removing a branch or patching a check can change semantics; preserve a reference binary and distinguish unpacking, emulation, and devirtualization.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. JUNK CODE & OPAQUE PREDICATES; 2. SELF-MODIFYING CODE (SMC); 3. CONTROL FLOW FLATTENING (CFF); 4. MOVFUSCATOR | [Read](./references/01-junk-code-opaque-predicates.md) |
| 5. VM PROTECTION (VMProtect / Themida / Code Virtualizer); 6. STRING ENCRYPTION; 7. IMPORT HIDING; 8. ANTI-DISASSEMBLY TRICKS; 9. DECISION TREE | [Read](./references/02-vm-protection-vmprotect-themida-code-virtualizer.md) |
| 10. TOOLBOX | [Read](./references/03-toolbox.md) |
