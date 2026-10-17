---
name: csp-bypass-advanced
description: >-
  Advanced Content Security Policy bypass techniques. Use when XSS or data
  exfiltration is blocked by CSP and you need to find policy weaknesses, trusted
  endpoint abuse, nonce leakage, or exfiltration channels that CSP cannot block.
---

# Csp Bypass Advanced

## Working approach

- Record every enforced policy, report-only policy, delivery mechanism, document context, and browser version
- Identify the actual script/navigation/resource sink and a permitted trust path
- Reproduce the effect in the browser under the complete policy set.

## Evidence and limits

The claimed script execution or data flow occurs despite the effective enforced directives.

Multiple policies intersect; missing base-uri, a JSONP URL, or strict-dynamic alone is not a universal bypass, and CSP does not replace fixing the underlying injection.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CSP DIRECTIVE REFERENCE MATRIX | [Read](./references/01-csp-directive-reference-matrix.md) |
| 2. BYPASS TECHNIQUES BY DIRECTIVE; 3. CSP IN META TAG vs. HEADER; 4. DATA EXFILTRATION DESPITE CSP | [Read](./references/02-bypass-techniques-by-directive.md) |
| 5. CSP BYPASS DECISION TREE; 6. TRICK NOTES — WHAT AI MODELS MISS | [Read](./references/03-csp-bypass-decision-tree.md) |
