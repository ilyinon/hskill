---
name: symbolic-execution-tools
description: >-
  Symbolic execution and constraint solving playbook. Use when solving CTF
  reversing challenges, recovering keys, bypassing checks, or automating
  binary analysis with angr, Z3, or Unicorn Engine.
---

# Symbolic Execution Tools

## Working approach

- Identify input source, architecture, calling convention, initialization, and success/failure conditions
- Choose Z3 for explicit constraints, angr for paths, or Unicorn for concrete regions
- Constrain input and hook only the behavior needed to keep the model faithful.

## Evidence and limits

A recovered input is accepted by the original local program or independently satisfies the original constraints.

A satisfiable symbolic model can reflect bad initialization or hooks; bitvector/integer sorts, endianness, path explosion, and unsupported calls must be checked.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ANGR — CORE CONCEPTS; 2. Z3 CONSTRAINT SOLVING | [Read](./references/01-angr-core-concepts.md) |
| 3. UNICORN ENGINE — CODE EMULATION; 4. ANGR EXPLORATION STRATEGIES; 5. PRACTICAL WORKFLOW; 6. DECISION TREE; 7. COMMON PITFALLS & FIXES; 8. TOOL VERSIONS & INSTALLATION | [Read](./references/02-unicorn-engine-code-emulation.md) |
| Advanced: angr Cookbook — Ready-to-Use Script Patterns for CTF Challenges | [Read](./ANGR_COOKBOOK.md) |
