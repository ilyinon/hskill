---
name: symmetric-cipher-attacks
description: >-
  Symmetric cipher attack playbook. Use when exploiting block cipher mode
  weaknesses (CBC padding oracle, ECB cut-and-paste, bit flipping), stream
  cipher key reuse, or meet-in-the-middle attacks.
---

# Symmetric Cipher Attacks

## Working approach

- Identify mode, block size, IV/nonce layout, padding, integrity protection, oracle, and known data
- Select the matching CBC/ECB/stream/PRNG hypothesis
- Validate recovered or modified values against independent plaintext and authentication behavior.

## Evidence and limits

The exact confidentiality, integrity, or state-recovery claim is reproduced under the stated construction.

Ciphertext length or a repeated block is not a complete attack; false padding positives, nonce uniqueness, prefix alignment, and IV indexing matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. PADDING ORACLE ATTACK (CBC MODE); 2. CBC BIT FLIPPING | [Read](./references/01-padding-oracle-attack-cbc-mode.md) |
| 3. ECB MODE ATTACKS; 4. STREAM CIPHER ATTACKS | [Read](./references/02-ecb-mode-attacks.md) |
| 5. MEET-IN-THE-MIDDLE; 6. DECISION TREE; 7. TOOLS | [Read](./references/03-meet-in-the-middle.md) |
| Advanced: Block Cipher Attacks — Detailed Scripts & Walkthrough | [Read](./BLOCK_CIPHER_ATTACKS.md) |
