---
name: dns-rebinding-attacks
description: >-
  DNS rebinding attack playbook. Use when testing applications that trust DNS resolution for origin checks, interact with internal services from browser context, or when SSRF is not possible server-side but the target has client-side fetch/XHR to attacker-controlled domains.
---

# Dns Rebinding Attacks

## Working approach

- Separate browser rebinding from server-side check/use resolution
- Record DNS answers, resolver caching, request timing, host checks, and destination policy
- Verify which address is used for validation and for the actual connection.

## Evidence and limits

A controlled hostname causes a permitted test client to cross the intended destination or origin boundary.

TTL zero does not force every resolver to re-resolve; host validation, pinning, browser local-network protections, and metadata token requirements remain independent.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE PRINCIPLE; 2. TTL MANIPULATION; 3. ATTACK VARIANTS; 4. HIGH-VALUE TARGETS | [Read](./references/01-core-principle.md) |
| 5. TOOLS; 6. DNS REBINDING vs. SSRF; 7. DEFENSES AND DEFENSE BYPASS; 8. DECISION TREE; 9. REAL-WORLD EXPLOITATION CHECKLIST | [Read](./references/02-tools.md) |
