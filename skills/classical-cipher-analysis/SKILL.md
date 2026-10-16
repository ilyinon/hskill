---
name: classical-cipher-analysis
description: >-
  Classical cipher analysis playbook. Use when encountering substitution
  ciphers, Vigenere, transposition, XOR, or encoded text in CTF challenges
  that requires frequency analysis, Kasiski examination, or known-plaintext
  cryptanalysis.
---

# Classical Cipher Analysis

## Working approach

- Identify encoding versus encryption, alphabet, length, statistics, and likely structure
- Select substitution, polyalphabetic, transposition, algebraic, or XOR analysis
- Test candidates against independent structure or known plaintext.

## Evidence and limits

A recovered key/transformation reproduces the ciphertext and yields independently plausible plaintext.

A readable fragment or matching frequency is not unique recovery; preserve alphabet conventions, padding, and multiple equivalent solutions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CIPHER IDENTIFICATION METHODOLOGY; 2. MONOALPHABETIC SUBSTITUTION | [Read](./references/01-cipher-identification-methodology.md) |
| 3. CAESAR / ROT CIPHERS; 4. VIGENERE CIPHER; 5. AFFINE CIPHER | [Read](./references/02-caesar-rot-ciphers.md) |
| 6. HILL CIPHER; 7. TRANSPOSITION CIPHERS; 8. XOR CIPHER; 9. SPECIAL CIPHERS | [Read](./references/03-hill-cipher.md) |
| 10. DECISION TREE; 11. TOOLS | [Read](./references/04-decision-tree.md) |
