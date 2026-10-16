---
name: type-juggling
description: >-
  PHP type juggling and weak comparison (`==`) bypass. Use when authentication, HMAC/signature checks, or token validation uses loose equality, numeric coercion, or hash comparisons without strict types — common in legacy PHP and CTF-style code paths.
---

# Type Juggling

## Working approach

- Identify PHP major version, exact operand types, comparison operator, and error handling
- Reproduce the relevant expression locally
- Distinguish magic numeric strings, boolean coercion, explicit casts, and invalid argument handling.

## Evidence and limits

Distinct security-relevant values compare as equal or an error path bypasses a required check in the actual code.

Legacy NULL-return tricks may throw TypeError on PHP 8; chained comparisons and MD5 collisions are different from magic-hash coercion.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. LOOSE COMPARISON (`==`) — TRUTH TABLE & VERSIONS; 2. MAGIC HASHES (`0e…` + digits only) | [Read](./references/01-quick-start.md) |
| 3. HMAC BYPASS (LOOSE COMPARE VS `"0"` OR `0`); 4. NULL JUGGLING (ARRAYS & TYPE ERRORS); 5. CTF PATTERNS; 6. DECISION TREE | [Read](./references/02-hmac-bypass-loose-compare-vs-0-or-0.md) |
