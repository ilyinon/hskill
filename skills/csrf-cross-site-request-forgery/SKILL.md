---
name: csrf-cross-site-request-forgery
description: >-
  CSRF testing playbook. Use when reviewing state-changing web flows, anti-CSRF defenses, SameSite behavior, JSON CSRF, login CSRF, and OAuth state handling.
---

# Csrf Cross Site Request Forgery

## Working approach

- Identify a meaningful state-changing operation and its authentication mechanism
- Compare the authorized request with a browser-sendable cross-origin request
- Verify cookies, SameSite, tokens, Origin checks, preflight, and final server state.

## Evidence and limits

A victim browser performs a forbidden state change under realistic session conditions without the intended anti-CSRF check.

A crafted request from curl/Burp or a missing token alone does not prove browser feasibility; self-only effects and CORS reads are separate issues.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPT; 2. FINDING CSRF TARGETS; 3. TOKEN BYPASS TECHNIQUES; 4. SAMESITE BYPASS SCENARIOS; 5. CSRF PROOF OF CONCEPT TEMPLATES; 6. JSON CSRF; 7. MULTIPART CSRF; 8. CSRF + XSS COMBINATION (CSRF Token Bypass) | [Read](./references/01-core-concept.md) |
| 9. OAUTH CSRF (STATE PARAMETER MISSING); 10. CSRF TESTING CHECKLIST; 11. JSON CSRF TECHNIQUES; 12. MULTIPART CSRF & CLIENT-SIDE PATH TRAVERSAL; 13. SAMESITE=LAX ADVANCED BYPASS TECHNIQUES; 14. ADVANCED JSON CSRF TECHNIQUES | [Read](./references/02-oauth-csrf-state-parameter-missing.md) |
| 15. CSRF + CORS MISCONFIGURATION CHAINS; 16. CSRF TOKEN FIXATION (PRE-SESSION TOKENS); 17. CLICKJACKING AS CSRF BYPASS | [Read](./references/03-csrf-cors-misconfiguration-chains.md) |
