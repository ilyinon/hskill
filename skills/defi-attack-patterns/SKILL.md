---
name: defi-attack-patterns
description: >-
  DeFi attack pattern playbook. Use when analyzing flash loan attacks, price oracle manipulation, MEV sandwich attacks, governance exploits, bridge vulnerabilities, and token standard edge cases in decentralized finance protocols.
---

# Defi Attack Patterns

## Working approach

- Pin chain state, contracts, dependencies, oracle design, and accounting invariants
- Model flash liquidity, transaction ordering, rounding, and privilege prerequisites
- Reproduce on a local fork with explicit balances before and after.

## Evidence and limits

The local transaction sequence violates a stated economic or authorization invariant after costs and repayment.

A flash loan or spot-price change alone is not profit; liquidity, slippage, fees, oracle windows, and reachable permissions can invalidate the chain.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. FLASH LOAN ATTACKS; 2. PRICE ORACLE MANIPULATION; 3. MEV (MAXIMAL EXTRACTABLE VALUE); 4. PRECISION LOSS EXPLOITATION | [Read](./references/01-flash-loan-attacks.md) |
| 5. GOVERNANCE ATTACKS; 6. BRIDGE EXPLOITS; 7. TOKEN STANDARD EDGE CASES; 8. NOTABLE DEFI EXPLOITS REFERENCE; 9. DECISION TREE | [Read](./references/02-governance-attacks.md) |
