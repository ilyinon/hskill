---
name: xss-cross-site-scripting
description: >-
  XSS playbook. Use when user-controlled content reaches HTML, attributes, JavaScript, DOM sinks, uploads, or multi-context rendering paths.
---

# Xss Cross Site Scripting

## Working approach

- Trace the source to its actual HTML, attribute, script, URL, or DOM sink and encoding stages
- Test a context-appropriate harmless marker in the real browser
- Verify attacker-controlled execution under effective sanitization and CSP.

## Evidence and limits

Controlled script executes in the protected origin/context through the demonstrated reachable data flow.

Reflection, a blocked tag, sanitizer presence, or markup injection alone is not XSS; browser parsing, frameworks, Trusted Types, and interaction requirements matter.

## Solving decisions

When a prerequisite is unclear or an attempt fails, use [diagnostics](./references/diagnostics.md) to choose the next discriminating check. For a complete change-of-approach example with controls and a checked result, read the matching [worked case](./references/worked-cases.md). Keep the requested goal and remaining unproved edges explicit.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. INJECTION CONTEXT MATRIX; 2. MULTI-REFLECTION ATTACKS; 3. ADVANCED INJECTION VECTORS | [Read](./references/01-injection-context-matrix.md) |
| 4. CSP BYPASS TECHNIQUES; 5. FILTER AND WAF BYPASS; 6. SECOND-ORDER XSS; 7. BLIND XSS METHODOLOGY; 8. XSS EXPLOITATION CHAIN; 9. DECISION TREE | [Read](./references/02-csp-bypass-techniques.md) |
| 10. XSS TESTING PROCESS (ZSEANO METHOD) | [Read](./references/03-xss-testing-process-zseano-method.md) |
| Advanced: Advanced XSS Tricks — Supplementary Reference | [Read](./ADVANCED_XSS_TRICKS.md) |
| Advanced: XSS — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
