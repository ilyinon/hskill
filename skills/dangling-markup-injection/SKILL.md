---
name: dangling-markup-injection
description: >-
  Dangling markup injection playbook. Use when HTML injection is possible but
  JavaScript execution is blocked (CSP, sanitizer strips event handlers, WAF
  blocks script tags) — exfiltrate CSRF tokens, session data, and page content
  by injecting unclosed HTML tags that capture subsequent page content.
---

# Dangling Markup Injection

## Working approach

- Identify the exact HTML insertion context, escaping, CSP, and sensitive following content
- Trace the browser's parsed DOM and outbound resource handling
- Use a benign marker and controlled destination to test the proposed leak.

## Evidence and limits

The browser transmits the intended following marker across the prohibited boundary under the tested policy.

An unterminated tag, reflected markup, or a permitted img-src does not prove leakage; parser repair, browser restrictions, and content position matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. WHEN TO USE DANGLING MARKUP; 2. CORE TECHNIQUE; 3. EXFILTRATION VECTORS; 4. WHAT CAN BE STOLEN; 5. BROWSER-SPECIFIC BEHAVIOR | [Read](./references/01-when-to-use-dangling-markup.md) |
| 6. ADVANCED TECHNIQUES; 7. LIMITATIONS; 8. COMBINATION ATTACKS; 9. DANGLING MARKUP DECISION TREE; 10. TRICK NOTES — WHAT AI MODELS MISS | [Read](./references/02-advanced-techniques.md) |
