---
name: vm-and-bytecode-reverse
description: >-
  Custom VM and bytecode reverse engineering playbook. Use when CTF challenges
  or protected software implement custom virtual machines with proprietary
  bytecode, dispatcher loops, or maze-style challenges.
---

# Vm And Bytecode Reverse

## Working approach

- Find the dispatcher and VM state rather than treating bytecode as native instructions
- Map opcode operands, widths, side effects, control flow, and I/O
- Extract the program and verify a small disassembler/emulator against native traces.

## Evidence and limits

Reconstructed semantics explain the observed execution and recovered inputs work in the original program.

A guessed opcode map or solver result is insufficient; signedness, overflow, self-modifying bytecode, nested dispatch, and initialization can change behavior.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CUSTOM VM IDENTIFICATION; 2. ANALYSIS METHODOLOGY | [Read](./references/01-custom-vm-identification.md) |
| 3. COMMON VM PATTERNS IN CTF; 4. MAZE CHALLENGES; 5. REAL-WORLD VM PROTECTORS | [Read](./references/02-common-vm-patterns-in-ctf.md) |
| 6. TOOLS; 7. DECISION TREE; 8. CTF SOLVING WORKFLOW | [Read](./references/03-tools.md) |
