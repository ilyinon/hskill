---
name: rsa-attack-techniques
description: >-
  RSA attack playbook for CTF and real-world cryptanalysis. Use when given
  RSA parameters (n, e, c) and need to recover plaintext by exploiting
  weak keys, small exponents, shared factors, or padding oracles.
---

# Rsa Attack Techniques

## Working approach

- Identify n/e/c, padding, message structure, shared keys/moduli, oracle behavior, and fault access
- Select the attack whose mathematical assumptions fit
- Verify recovered factors, plaintext, or signatures using the original RSA equations and encoding.

## Evidence and limits

The recovered candidate satisfies the construction and independent constraints.

Raw RSA equations are not equivalent to OAEP/PSS behavior; a small exponent, shared modulus, or oracle-looking error is not sufficient without the required conditions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. FACTORIZATION ATTACKS; 2. SMALL EXPONENT ATTACKS; 3. LARGE e / SMALL d ATTACKS | [Read](./references/01-factorization-attacks.md) |
| 4. COPPERSMITH'S METHOD; 5. COMMON MODULUS ATTACK; 6. ORACLE ATTACKS; 7. RSA-CRT FAULT ATTACK; 8. DECISION TREE | [Read](./references/02-coppersmith-s-method.md) |
| 9. TOOLS | [Read](./references/03-tools.md) |
| Advanced: RSA Attack Catalog — Detailed Implementations & Mathematics | [Read](./RSA_ATTACK_CATALOG.md) |
