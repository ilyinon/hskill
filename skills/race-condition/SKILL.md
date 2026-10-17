---
name: race-condition
description: >-
  Race condition and TOCTOU testing for web apps. Use when testing one-time operations, concurrent HTTP abuse, rate-limit bypass, Turbo Intruder gates, HTTP/2 single-packet attacks, and CWE-362-style synchronization gaps.
---

# Race Condition

## Working approach

- Define the single-use or accounting invariant and a sequential baseline using owned objects
- Identify the check/use or transaction boundary
- Perform a bounded synchronized test, then inspect durable state and repeat controls.

## Evidence and limits

Concurrent execution violates the invariant beyond the sequential baseline with reproducible committed effects.

Multiple success responses may be retries or eventual consistency; bound request count and avoid financial/stock effects outside authorized fixtures.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START — What to Test First; 1. CORE CONCEPT; 2. ATTACK PATTERNS; 3. HTTP/1.1 LAST-BYTE SYNCHRONIZATION; 4. HTTP/2 SINGLE-PACKET ATTACK | [Read](./references/01-quick-start-what-to-test-first.md) |
| 5. TURBO INTRUDER TEMPLATES; 6. CVE REFERENCE — CVE-2022-4037; 7. TOOLS; 8. DECISION TREE | [Read](./references/02-turbo-intruder-templates.md) |
| 9. HTTP/2 SINGLE-PACKET ATTACK — DETAILED MECHANICS; 10. DATABASE ISOLATION LEVEL EXPLOITATION MATRIX | [Read](./references/03-http-2-single-packet-attack-detailed-mechanics.md) |
| 11. LIMIT-OVERRUN ATTACK PATTERNS; 12. SINGLE-PACKET MULTI-ENDPOINT ATTACK; Related | [Read](./references/04-limit-overrun-attack-patterns.md) |
