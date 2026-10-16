---
name: jwt-oauth-token-attacks
description: >-
  JWT and OAuth token attack playbook. Use when validating token trust, signing algorithms, key handling, claim abuse, bearer flows, and OAuth account-binding weaknesses.
---

# Jwt Oauth Token Attacks

## Working approach

- Identify token type, signing verification, key source, issuer/audience, and resulting identity
- Separate JWT validation from OAuth flow/binding checks
- Compare an accepted baseline with a single controlled mutation and inspect the resulting authorization.

## Evidence and limits

A token or flow that violates the required trust policy is accepted and grants a demonstrated identity/capability.

Decoding, changing an unsigned claim, or possessing another valid token is not forgery; URL fragments are not sent in the Referer header.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. JWT ANATOMY; 2. ATTACK 1 — ALGORITHM NONE (alg:none); 3. ATTACK 2 — RS256 TO HS256 KEY CONFUSION; 4. ATTACK 3 — JWT SECRET BRUTE FORCE; 5. ATTACK 4 — kid (Key ID) INJECTION; 6. ATTACK 5 — jku / x5u Header Injection; 7. OAUTH 2.0 — STATE PARAMETER MISSING (CSRF) | [Read](./references/01-jwt-anatomy.md) |
| 8. OAUTH — REDIRECT_URI BYPASS; 9. OAUTH — IMPLICIT FLOW TOKEN THEFT; 10. OAUTH — SCOPE ESCALATION; 11. TOKEN LEAKAGE VECTORS; 12. JWT TESTING CHECKLIST; 13. OAUTH TESTING CHECKLIST | [Read](./references/02-oauth-redirect-uri-bypass.md) |
