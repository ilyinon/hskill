---
name: anti-debugging-techniques
description: >-
  Anti-debugging detection and bypass playbook. Use when reversing protected
  binaries that detect debuggers via ptrace, PEB flags, timing checks, or
  signal/exception handlers on Linux and Windows.
---

# Anti Debugging Techniques

## Working approach

- Identify OS, architecture, debugger, and the exact detection branch
- Compare normal and instrumented execution
- Change one detector in an isolated copy and verify the program's original behavior remains meaningful.

## Evidence and limits

The identified check explains the observed failure, and a controlled countermeasure restores the relevant analysis path.

Timing differences, exceptions, or a crash alone do not identify anti-debugging; overlapping integrity and environment checks may remain.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. LINUX ANTI-DEBUG TECHNIQUES | [Read](./references/01-linux-anti-debug-techniques.md) |
| 2. WINDOWS ANTI-DEBUG TECHNIQUES; 3. ADVANCED MULTI-LAYER TECHNIQUES; 4. COUNTERMEASURE TOOLS; 5. SYSTEMATIC BYPASS METHODOLOGY | [Read](./references/02-windows-anti-debug-techniques.md) |
| 6. DECISION TREE; 7. CTF & REAL-WORLD PATTERNS; 8. QUICK REFERENCE — BYPASS CHEAT SHEET | [Read](./references/03-decision-tree.md) |
| Advanced: Anti-Debug Technique × OS × Detection × Bypass — Comprehensive Matrix | [Read](./ANTI_DEBUG_MATRIX.md) |
