---
name: open-redirect
description: >-
  Open redirect playbook. Use when URL parameters, form actions, or JavaScript sinks control navigation targets and may redirect users to attacker-controlled destinations.
---

# Open Redirect

## Working approach

- Identify the redirect sink and whether the server, browser, or framework normalizes the destination
- Test a controlled benign external destination and capture the effective navigation
- Validate any OAuth, SSRF, or trust-chain impact separately.

## Evidence and limits

Untrusted input causes navigation to a destination outside the intended redirect policy.

A reflected URL or a 3xx status alone does not show an external redirect; redirect reachability does not automatically imply token theft or SSRF.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPT; 2. FINDING REDIRECT PARAMETERS; 3. FILTER BYPASS TECHNIQUES; 4. EXPLOITATION CHAINS; 5. TESTING CHECKLIST; 6. TABNABBING (REVERSE TABNABBING); 7. OPEN REDIRECT → OAUTH TOKEN THEFT (DETAILED CHAINS) | [Read](./references/01-core-concept.md) |
| 8. OPEN REDIRECT → SSRF CHAIN; 9. URL PARSER CONFUSION FOR REDIRECT BYPASS | [Read](./references/02-open-redirect-ssrf-chain.md) |
