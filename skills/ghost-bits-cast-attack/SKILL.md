---
name: ghost-bits-cast-attack
description: >-
  Analyze Java character-to-byte narrowing and parser differentials when validation and a downstream consumer may interpret the same input differently.
---

# Ghost Bits Cast Attack

## Working approach

- Locate a concrete character-to-byte narrowing, permissive decoding, or parser-normalization mismatch
- Identify which representation the validator and consumer use
- Reproduce the differential with benign characters on the exact component version.

## Evidence and limits

Validation and use interpret the same input differently and a reachable sink gives that mismatch a demonstrated effect.

Unicode variants alone do not bypass a patched vulnerability; WAF matching, downstream parsing, and vulnerable sink reachability are separate conditions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ONE-MINUTE MENTAL MODEL | [Read](./references/01-one-minute-mental-model.md) |
| 2. THREE ROOT-CAUSE FAMILIES; 3. CHARACTER GENERATOR | [Read](./references/02-three-root-cause-families.md) |
| 4. DANGEROUS-BYTE TO GHOST-CHARACTER MAP; 5. PER-COMPONENT PAYLOAD RECIPES | [Read](./references/03-dangerous-byte-to-ghost-character-map.md) |
| 5.3 Jackson `charToHex` — SQLi smuggling (Family C); 5.4 Fastjson — `\u` and `\x` escape bypass (Families B + C); 5.5 Spring / Jetty / Undertow / Vert.x — URL decoding (Families A + B); 5.6 Angus Mail / Jakarta Mail — SMTP injection (Family A); 5.7 Apache HttpClient `<= 4.5.9` — request smuggling (Family A); 5.8 JDK HttpServer — response splitting (CVE-2026-21933, Family A); 5.9 Other affected components | [Read](./references/04-3-jackson-chartohex-sqli-smuggling-family-c.md) |
| 6. KNOWN-CVE BYPASS RECIPES; 7. DETECTION DECISION TREE; 8. SAST / CODE-AUDIT SIGNATURES | [Read](./references/05-known-cve-bypass-recipes.md) |
| 9. DIFFERENTIAL TESTING WORKFLOW; 10. DEFENSE AWARENESS; 11. QUICK REFERENCE — KEY PAYLOADS; REFERENCES | [Read](./references/06-differential-testing-workflow.md) |
| Advanced: Ghost Bits Cast Attack — Payload Cookbook | [Read](./PAYLOAD_COOKBOOK.md) |
