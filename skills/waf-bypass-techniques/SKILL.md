---
name: waf-bypass-techniques
description: >-
  WAF bypass methodology and generic evasion techniques. Use when a web application
  firewall blocks injection payloads (SQLi, XSS, RCE) and you need to craft
  bypasses using encoding, protocol-level tricks, or WAF-specific weaknesses.
---

# Waf Bypass Techniques

## Working approach

- Establish a reproducible blocked baseline and identify WAF versus application behavior
- Choose one encoding, framing, content-type, or normalization hypothesis supported by the actual parser chain
- Verify the original vulnerability's effect after the request reaches the application.

## Evidence and limits

The application receives the intended interpretation and the claimed security impact is demonstrated under the tested rule set.

A 200, changed block page, vendor fingerprint, or payload accepted by WAF is not successful exploitation; vendor matrices are configuration/version-specific hypotheses.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. PHASE 0 — IDENTIFY THE WAF | [Read](./references/01-phase-0-identify-the-waf.md) |
| 2. GENERIC BYPASS CATEGORIES; 3. PROTOCOL-LEVEL BYPASS TECHNIQUES | [Read](./references/02-generic-bypass-categories.md) |
| 4. WAF BYPASS DECISION TREE; 5. COMMON MISTAKES & TRICK NOTES; 6. DEFENSE PERSPECTIVE | [Read](./references/03-waf-bypass-decision-tree.md) |
| Advanced: WAF Product Bypass Matrix | [Read](./WAF_PRODUCT_MATRIX.md) |
