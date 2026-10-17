---
name: email-header-injection
description: >-
  Email header injection and spoofing playbook. Use when testing contact forms, email APIs, password reset flows, or any feature that constructs SMTP messages with user-controlled fields. Covers CRLF injection in headers, SPF/DKIM/DMARC bypass, and phishing amplification.
---

# Email Header Injection

## Working approach

- Trace user fields into message headers, envelope addresses, MIME parts, or templates
- Identify library normalization and transport
- Compare a harmless marker against the resulting raw message and delivery behavior in a test mailbox.

## Evidence and limits

An untrusted field changes a protected header, recipient, MIME structure, or rendered content beyond intended policy.

Newlines rejected by a library are not injection; SPF, DKIM, DMARC, display-name spoofing, and header injection establish different claims.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SMTP HEADER INJECTION FUNDAMENTALS; 2. ATTACK SCENARIOS; 3. COMMON VULNERABLE PATTERNS | [Read](./references/01-smtp-header-injection-fundamentals.md) |
| 4. SPF / DKIM / DMARC BYPASS TECHNIQUES; 5. MAIL CLIENT RENDERING ATTACKS; 6. CONTACT FORM / EMAIL API INJECTION; 7. TESTING METHODOLOGY; 8. DECISION TREE | [Read](./references/02-spf-dkim-dmarc-bypass-techniques.md) |
| 9. QUICK REFERENCE — KEY PAYLOADS | [Read](./references/03-quick-reference-key-payloads.md) |
