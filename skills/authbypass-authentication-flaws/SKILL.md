---
name: authbypass-authentication-flaws
description: >-
  Authentication bypass testing playbook. Use when assessing login flows, password reset logic, account recovery, MFA bypass, token predictability, brute-force resistance, and session boundary flaws.
---

# Authbypass Authentication Flaws

## Working approach

- Map login, registration, reset, MFA, account linking, and session issuance
- Establish the test identity and lockout constraints
- Follow the state transition through issuance and server-side authorization.

## Evidence and limits

A permitted test obtains or uses an identity/session capability without the required authentication or binding check.

OTP delivery, CAPTCHA completion, different errors, or changing to a valid administrator session are not account takeover; avoid lockout-prone guessing.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. AUTHORIZED CREDENTIAL TEST PLANNING; 1. SQL INJECTION LOGIN BYPASS; 2. PASSWORD RESET VULNERABILITIES; 3. ACCOUNT ENUMERATION; 4. BRUTE FORCE BYPASS | [Read](./references/01-authorized-credential-test-planning.md) |
| 5. MULTI-FACTOR AUTHENTICATION BYPASS; 6. OAUTH / SSO ACCOUNT TAKEOVER PATTERNS; 7. USERNAME / PASSWORD FIELD MANIPULATION; 8. SESSION MANAGEMENT FLAWS; 9. AUTHENTICATION TESTING CHECKLIST; 10. PASSWORD RESET ATTACK MATRIX (22 Patterns) | [Read](./references/02-multi-factor-authentication-bypass.md) |
| 11. CAPTCHA/VERIFICATION BYPASS PATTERNS (20 Methods); 12. INSECURE RANDOMNESS — TOKEN PREDICTION | [Read](./references/03-captcha-verification-bypass-patterns-20-methods.md) |
