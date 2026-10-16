---
name: business-logic-vulnerabilities
description: >-
  Business logic vulnerability playbook. Use when reasoning about workflows, race conditions, price manipulation, coupon abuse, state machines, and multi-step authorization gaps.
---

# Business Logic Vulnerabilities

## Working approach

- Model actors, object ownership, states, allowed transitions, and value invariants
- Compare normal and altered sequences using owned test objects
- Inspect alternate APIs, concurrency, and downstream effects only where the business model supports them.

## Evidence and limits

The unchanged test principal breaks a defined authorization, state, quota, or value invariant with observable server-side effect.

A success message, UI bypass, or valid admin session is not a logic flaw; assess intended policy and final state, and keep financial tests within permitted fixtures.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. PRICE AND VALUE MANIPULATION | [Read](./references/01-price-and-value-manipulation.md) |
| 2. RACE CONDITIONS; 3. WORKFLOW / STEP SKIP BYPASS; 4. COUPON AND REFERRAL ABUSE | [Read](./references/02-race-conditions.md) |
| 5. ACCOUNT / PRIVILEGE LOGIC FLAWS; 6. API BUSINESS LOGIC FLAWS; 7. SUBSCRIPTION / TIER CONFUSION | [Read](./references/03-account-privilege-logic-flaws.md) |
| 8. FILE UPLOAD BUSINESS LOGIC; 9. TESTING APPROACH; 10. HIGH-IMPACT CHECKLISTS; 11. CONSOLIDATED CHECKLIST (2-Hour Full Sweep) | [Read](./references/04-file-upload-business-logic.md) |
| 11.5 Payment / Order; 11.6 IDOR / Authorization; 11.7 CAPTCHA / Verification Code; 11.8 File Upload; 11.9 CSRF / SSRF / XXE; How to Use This Section | [Read](./references/05-5-payment-order.md) |
| Advanced: Business Logic Vulnerability Checklist / 业务逻辑漏洞检查清单 | [Read](./CHECKLIST.md) |
| Advanced: Business Logic Vulnerability Testing Methodology / 业务逻辑漏洞测试方法论 | [Read](./METHODOLOGY.md) |
| Advanced: Business Logic Vulnerabilities — Extended Scenarios | [Read](./SCENARIOS.md) |
