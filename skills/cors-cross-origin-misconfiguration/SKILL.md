---
name: cors-cross-origin-misconfiguration
description: >-
  CORS misconfiguration testing playbook. Use when analyzing cross-origin trust, credentialed browser reads, origin reflection, preflight policy bugs, and browser-based access to authenticated APIs.
---

# Cors Cross Origin Misconfiguration

## Working approach

- Capture the effective CORS policy for a sensitive response
- Reproduce an attacker-origin browser request with realistic cookies and SameSite behavior
- Verify whether script can read protected content.

## Evidence and limits

The attacker-controlled origin reads a response forbidden by the intended origin and identity policy.

Header reflection or curl success alone is insufficient; wildcard ACAO with credentials does not permit credentialed browser reads.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. WHEN TO LOAD THIS SKILL; 2. HIGH-VALUE MISCONFIGURATION CHECKS; 3. QUICK TRIAGE; 4. RELATED ROUTES; 5. NULL ORIGIN EXPLOITATION; 6. SUBDOMAIN XSS → CORS BYPASS CHAIN; 7. VARY: ORIGIN CACHING ISSUE | [Read](./references/01-when-to-load-this-skill.md) |
| 8. REGEX BYPASS PATTERNS; 9. INTERNAL NETWORK CORS EXPLOITATION | [Read](./references/02-regex-bypass-patterns.md) |
| Advanced: CORS Misconfiguration — Extended Scenarios | [Read](./SCENARIOS.md) |
