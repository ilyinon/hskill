---
name: stack-overflow-and-rop
description: >-
  Stack overflow and ROP playbook. Use when exploiting buffer overflows to hijack control flow via return address overwrite, ROP chains, ret2libc, ret2csu, ret2dlresolve, or SROP on Linux userland binaries.
---

# Stack Overflow And Rop

## Working approach

- Identify architecture/ABI, overflow offset, actual control, leaks, and enabled protections
- Select a chain from available gadgets and exact runtime structures
- Validate argument setup, stack alignment, and the intended local effect.

## Evidence and limits

The local reproduction controls the intended instruction path and produces the claimed bounded effect.

A crash or overwritten return address alone is not a working chain; ret2csu availability, libc symbols/hooks, gadget constraints, and syscalls vary by build.

## Solving decisions

When a prerequisite is unclear or an attempt fails, use [diagnostics](./references/diagnostics.md) to choose the next discriminating check. For a complete change-of-approach example with controls and a checked result, read the matching [worked case](./references/worked-cases.md). Keep the requested goal and remaining unproved edges explicit.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. STACK LAYOUT FUNDAMENTALS; 2. RETURN-TO-LIBC; 3. ROP CHAIN CONSTRUCTION; 4. ret2csu — Universal 3-Argument Control | [Read](./references/01-stack-layout-fundamentals.md) |
| 5. ret2dlresolve; 6. SROP — Sigreturn-Oriented Programming; 7. STACK PIVOTING; 8. CANARY BYPASS; 9. TOOLS QUICK REFERENCE; 10. DECISION TREE | [Read](./references/02-ret2dlresolve.md) |
| Advanced: Advanced ROP Techniques — BROP, Partial Overwrite, JOP, COP | [Read](./ROP_ADVANCED_TECHNIQUES.md) |
