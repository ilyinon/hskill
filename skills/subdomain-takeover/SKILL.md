---
name: subdomain-takeover
description: >-
  Subdomain takeover detection and exploitation playbook. Use when targets have
  dangling CNAME/NS/MX records pointing to deprovisioned cloud resources, expired
  third-party services, or unclaimed SaaS tenants that an attacker can register
  to serve content under the victim's domain.
---

# Subdomain Takeover

## Working approach

- Resolve the full DNS chain and identify the actual provider/resource lifecycle
- Distinguish stale configuration from a claimable resource and verify provider restrictions
- Use non-mutating evidence unless a claim is explicitly permitted.

## Evidence and limits

The exact resource behind the target name is demonstrably unclaimed and claimable under the provider's current controls, or a permitted claim proves control.

NXDOMAIN, a branded error, or NoSuchBucket alone is a candidate; domain verification, reservations, region rules, and mail-domain ownership can prevent takeover.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPT; 2. DETECTION METHODOLOGY; 3. SERVICE PROVIDER FINGERPRINT TABLE; 4. TAKEOVER PROCEDURE — COMMON PROVIDERS; 5. NS TAKEOVER — HIGH SEVERITY | [Read](./references/01-core-concept.md) |
| 6. MX TAKEOVER — EMAIL INTERCEPTION; 7. WILDCARD DNS RISKS; 8. DETECTION & EXPLOITATION DECISION TREE; 9. DEFENSE & REMEDIATION; 10. TRICK NOTES — WHAT AI MODELS MISS | [Read](./references/02-mx-takeover-email-interception.md) |
