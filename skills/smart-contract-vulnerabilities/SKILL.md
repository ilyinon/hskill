---
name: smart-contract-vulnerabilities
description: >-
  Smart contract vulnerability playbook. Use when auditing Solidity/EVM contracts for reentrancy, integer overflow, access control, delegatecall, flash loan, signature replay, and MEV-related attack patterns.
---

# Smart Contract Vulnerabilities

## Working approach

- Pin compiler, deployed bytecode, chain/fork state, upgradeability, and privileged roles
- Define authorization, accounting, and call-order invariants
- Reproduce the specific path with owned actors on a local fork and inspect final state.

## Evidence and limits

A reachable transaction sequence violates the specified invariant under actual deployment semantics.

A pattern match is not exploitability; compiler checks, external-call behavior, proxy storage, token quirks, and chain/EVM upgrades affect the claim.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. REENTRANCY; 2. INTEGER OVERFLOW / UNDERFLOW; 3. ACCESS CONTROL; 4. RANDOMNESS MANIPULATION; 5. DELEGATECALL VULNERABILITIES; 6. FRONT-RUNNING / MEV | [Read](./references/01-reentrancy.md) |
| 7. SIGNATURE REPLAY; 8. SELF-DESTRUCT & FORCE-SEND ETH; 9. CREATE2 & DETERMINISTIC ADDRESS EXPLOITATION; 10. FLASH LOAN ATTACK PATTERNS; 11. SHORT ADDRESS ATTACK; 12. TOOLS; 13. DECISION TREE | [Read](./references/02-signature-replay.md) |
| Advanced: Solidity Vulnerability Patterns — Code Reference | [Read](./SOLIDITY_VULN_PATTERNS.md) |
