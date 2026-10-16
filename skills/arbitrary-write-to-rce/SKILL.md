---
name: arbitrary-write-to-rce
description: >-
  Arbitrary write to RCE playbook. Use when you have an arbitrary write primitive (from heap exploitation, format string, or OOB write) and need to convert it into code execution by targeting GOT, hooks, _IO_FILE vtable, exit_funcs, TLS_dtor_list, modprobe_path, .fini_array, or C++ vtables.
---

# Arbitrary Write To Rce

## Working approach

- Characterize write width, value/address control, repetition, leaks, and trigger
- Identify ABI, allocator/runtime version, relocation protections, and available targets
- Choose a reachable control-flow target whose integrity checks can be satisfied.

## Evidence and limits

The write reaches the intended target and a controlled local trigger produces the claimed execution effect.

A historical hook, vtable, or writable address is not automatically usable on the current build; preserve exact runtime constraints.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. TARGET SELECTION BY GLIBC VERSION; 2. GOT OVERWRITE; 3. __malloc_hook / __free_hook (glibc < 2.34); 4. _IO_FILE VTABLE; 5. __exit_funcs / __atexit | [Read](./references/01-target-selection-by-glibc-version.md) |
| 6. TLS_dtor_list (glibc ≥ 2.34); 7. _dl_fini / LINK_MAP CORRUPTION; 8. modprobe_path (KERNEL); 9. .fini_array; 10. C++ VTABLE OVERWRITE; 11. setcontext GADGET | [Read](./references/02-tls-dtor-list-glibc-2-34.md) |
| 12. DECISION TREE | [Read](./references/03-decision-tree.md) |
