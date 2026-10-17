---
name: ssti-server-side-template-injection
description: >-
  SSTI playbook. Use when template expressions, server-side rendering, preview features, or templating engines may evaluate attacker-controlled content.
---

# Ssti Server Side Template Injection

## Working approach

- Establish whether user input becomes template source or only data
- Compare harmless evaluation with literal and invalid-expression controls
- Identify engine, integration, sandbox, and version before selecting engine-specific techniques.

## Evidence and limits

Server-side template evaluation of controlled syntax is demonstrated and each additional disclosure or execution claim is separately supported.

Client-side interpolation, arithmetic output, or a stack trace alone does not prove a particular engine or RCE; Python attribute tricks are not universal Jinja sandbox escapes.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. DETECTION — POLYGLOT PROBE SEQUENCE; 2. ENGINE-TO-LANGUAGE MAPPING; 3. JINJA2 (PYTHON FLASK) — RCE CHAINS; 4. JINJA2 SANDBOX BYPASS TECHNIQUES | [Read](./references/01-detection-polyglot-probe-sequence.md) |
| 5. FREEMARKER (JAVA) — RCE; 6. TWIG (PHP) — RCE; 7. VELOCITY (JAVA) — RCE; 8. ERB (RUBY RAILS) — RCE; 9. THYMELEAF (JAVA SPRING) — RCE; 10. CLIENT-SIDE TEMPLATE INJECTION (AngularJS); 11. SSTI → FULL RCE PATH; 12. COMMON INJECTION ENTRY POINTS; 13. UNIVERSAL DETECTION PAYLOADS; 14. BLIND SSTI TECHNIQUES; 15. FLASK PIN CALCULATION | [Read](./references/02-freemarker-java-rce.md) |
| Advanced: ENGINE_PAYLOADS.md — Extended SSTI Fingerprinting & Payload Matrix | [Read](./ENGINE_PAYLOADS.md) |
| Advanced: SSTI — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
