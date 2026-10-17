---
name: recon-and-methodology
description: >-
  Reconnaissance and methodology playbook. Use when mapping assets, discovering endpoints, fingerprinting technology, and building a structured testing plan for a new target.
---

# Recon And Methodology

## Working approach

- Start from the authorized asset list and product context
- Collect passive clues and captured traffic before targeted active enumeration
- Deduplicate provenance-linked hosts, services, routes, identities, and object relationships.

## Evidence and limits

The inventory identifies reachable in-scope surfaces and supports a prioritized, evidence-based next check.

Ownership, DNS names, fingerprints, banners, and scanner matches are leads; record out-of-scope assets without silently probing them.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. RECON HIERARCHY; 2. SUBDOMAIN ENUMERATION (CRITICAL FIRST STEP); 3. SERVICE AND PORT DISCOVERY; 4. WEB TECHNOLOGY FINGERPRINTING; 5. ENDPOINT DISCOVERY; 6. SOURCE CODE RECON | [Read](./references/01-recon-hierarchy.md) |
| 7. ZSEANO'S TESTING METHODOLOGY; 8. BUG BOUNTY PROGRAM TRIAGE (WHERE TO SPEND TIME); 9. NUCLEI TEMPLATES (AUTOMATED SCANNING); 10. COMMON MISCONFIGURATIONS (QUICK WINS); 11. QUICK REFERENCE TOOLS; 12. JAVA MIDDLEWARE FINGERPRINT MATRIX; 13. INFORMATION LEAK DETECTION CHECKLIST | [Read](./references/02-zseano-s-testing-methodology.md) |
