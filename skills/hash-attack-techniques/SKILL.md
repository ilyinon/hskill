---
name: hash-attack-techniques
description: >-
  Hash attack playbook. Use when exploiting length extension, MD5/SHA1
  collisions, HMAC timing leaks, birthday attacks, or hash-based proof
  of work in CTF and authorized testing scenarios.
---

# Hash Attack Techniques

## Working approach

- Identify the construction, digest, key placement, salt, known data, and oracle
- Distinguish collision, preimage, length extension, key guessing, and timing hypotheses
- Verify the recovered or forged value against an independent check.

## Evidence and limits

The exact integrity or recovery claim is reproduced for the stated construction and inputs.

A collision does not imply preimage recovery or HMAC forgery; digest format and network timing alone do not establish the cryptographic weakness.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. LENGTH EXTENSION ATTACK; 2. MD5 COLLISION ATTACKS | [Read](./references/01-length-extension-attack.md) |
| 3. SHA-1 COLLISION; 4. BIRTHDAY ATTACK; 5. HMAC TIMING ATTACK; 6. MEET-IN-THE-MIDDLE (HASH); 7. HASH PROOF-OF-WORK; 8. RAINBOW TABLES & SALTING | [Read](./references/02-sha-1-collision.md) |
| 9. DECISION TREE; 10. TOOLS | [Read](./references/03-decision-tree.md) |
