---
name: ssrf-server-side-request-forgery
description: >-
  SSRF playbook. Use when the server fetches URLs, resolves hostnames, imports remote content, or can be driven toward internal networks, cloud metadata, or secondary protocols.
---

# Ssrf Server Side Request Forgery

## Working approach

- Identify the server-side fetcher, allowed schemes, redirect handling, DNS resolution, and destination policy
- Use a unique benign callback to attribute the request
- Test an owned restricted destination only when the authorization boundary permits it.

## Evidence and limits

The server makes an attributable request outside the intended destination policy; response read, internal reachability, and execution are separate impact claims.

DNS-only callbacks, client-side browser requests, and timing alone do not prove full SSRF impact; IMDSv2 still requires its token flow and headers even if DNS rebinding bypasses an address check.

## Solving decisions

When a prerequisite is unclear or an attempt fails, use [diagnostics](./references/diagnostics.md) to choose the next discriminating check. For a complete change-of-approach example with controls and a checked result, read the matching [worked case](./references/worked-cases.md). Keep the requested goal and remaining unproved edges explicit.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. FINDING SSRF SURFACE; 2. BASIC CONFIRMATION METHODOLOGY; 3. CLOUD METADATA ENDPOINTS — MUST-TRY | [Read](./references/01-quick-start.md) |
| 4. IP ADDRESS FILTER BYPASS TECHNIQUES; 5. URL SCHEME ATTACKS; 6. BLIND SSRF DETECTION; 7. INTERNAL SERVICE EXPLOITATION; 8. SSRF + FILTER BYPASS DECISION TREE | [Read](./references/02-ip-address-filter-bypass-techniques.md) |
| 9. THE SSRF-FILTER MINDSET | [Read](./references/03-the-ssrf-filter-mindset.md) |
| Advanced: SSRF — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
| Advanced: URL Parser Differentials & Advanced SSRF Techniques | [Read](./URL_PARSER_TRICKS.md) |
