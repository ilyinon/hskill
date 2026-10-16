---
name: idor-broken-object-authorization
description: >-
  IDOR and broken object authorization testing playbook. Use when requests expose object identifiers, tenant boundaries, writable fields, or missing object-level authorization checks.
---

# Idor Broken Object Authorization

## Working approach

- Define the subject/object/action/tenant policy using owned accounts and objects
- Hold the requesting identity fixed while changing only the target or function
- Compare authorized, denied, and cross-object requests including child resources.

## Evidence and limits

The unchanged principal reads or changes a protected object/function contrary to the intended policy.

Another valid user's or admin's session changes the principal; public resources, opaque IDs, and enumeration alone do not establish IDOR.

## Solving decisions

When a prerequisite is unclear or an attempt fails, use [diagnostics](./references/diagnostics.md) to choose the next discriminating check. For a complete change-of-approach example with controls and a checked result, read the matching [worked case](./references/worked-cases.md). Keep the requested goal and remaining unproved edges explicit.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. IDOR vs BOLA vs BFLA; 2. WHERE TO FIND OBJECT IDs (ALL LOCATIONS); 3. A-B TESTING METHODOLOGY; 4. ID TYPE ITS IMPLICATIONS; 5. HORIZONTAL vs VERTICAL PRIVILEGE ESCALATION; 6. HTTP METHOD ESCALATION; 7. PARAMETER POLLUTION & TYPE CONFUSION; 8. BFLA (FUNCTION LEVEL) ATTACKS; 9. INDIRECT IDOR (REFERENCE CHAIN) | [Read](./references/01-idor-vs-bola-vs-bfla.md) |
| 10. MASS ASSIGNMENT → PRIVILEGE ESCALATION; 11. STATE MACHINE ABUSE (BUSINESS LOGIC IDOR); 12. QUICK IDOR CHECKLIST; 13. SYSTEMATIC IDOR TESTING — 8 CATEGORIES; 14. ORM FILTER CHAIN LEAKS | [Read](./references/02-mass-assignment-privilege-escalation.md) |
