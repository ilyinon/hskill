---
name: lattice-crypto-attacks
description: >-
  Lattice-based cryptanalysis playbook. Use when attacking RSA via Coppersmith
  small roots, recovering DSA/ECDSA nonces from bias, solving knapsack
  problems, or applying LLL/BKZ reduction to cryptographic constructions.
---

# Lattice Crypto Attacks

## Working approach

- Express the exact algebraic relations, modulus, leaked bits, unknown bounds, and sample count
- Select SVP/CVP, Coppersmith, or HNP only when the assumptions fit
- Construct the lattice and verify candidate solutions against the original equations.

## Evidence and limits

Recovered unknowns satisfy the original construction and independent validation data.

LLL returning a short vector does not establish the desired solution; scaling, dimensions, bounds, numerical behavior, and sample independence matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. LATTICE FUNDAMENTALS; 2. LLL ALGORITHM; 3. BKZ (BLOCK KORKINE-ZOLOTAREV) | [Read](./references/01-lattice-fundamentals.md) |
| 4. COPPERSMITH'S METHOD; 5. HIDDEN NUMBER PROBLEM (HNP) — DSA/ECDSA NONCE RECOVERY; 6. KNAPSACK / SUBSET SUM ATTACKS | [Read](./references/02-coppersmith-s-method.md) |
| 7. NTRU CRYPTANALYSIS; 8. CONSTRUCTING ATTACK LATTICES — METHODOLOGY; 9. DECISION TREE; 10. COMMON PITFALLS | [Read](./references/03-ntru-cryptanalysis.md) |
