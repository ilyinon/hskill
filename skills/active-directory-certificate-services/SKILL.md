---
name: active-directory-certificate-services
description: >-
  AD Certificate Services attack playbook. Use when targeting misconfigured AD CS for privilege escalation via ESC1-ESC13 template abuse, NTLM relay to enrollment, CA officer abuse, and certificate-based persistence.
---

# Active Directory Certificate Services

## Working approach

- Record CA/template configuration, enrollment rights, issuance requirements, EKUs, and patch state
- Select an ESC path whose prerequisites are actually present
- Separate issuance from mapping and authentication.

## Evidence and limits

The issued certificate maps to the intended test identity and enables a capability outside the starting principal's policy.

Template flags alone do not establish exploitability; certificate mapping, approval, enrollment rights, and mitigations can break the chain.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. AD CS ARCHITECTURE OVERVIEW; 2. ENUMERATION; 3. ESC1 — ENROLLEE SUPPLIES SUBJECT; 4. ESC2 — ANY PURPOSE EKU; 5. ESC3 — ENROLLMENT AGENT; 6. ESC4 — TEMPLATE ACL MISCONFIGURATION; 7. ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2; 8. ESC7 — CA OFFICER / MANAGER PERMISSIONS; 9. ESC8 — NTLM RELAY TO HTTP ENROLLMENT | [Read](./references/01-ad-cs-architecture-overview.md) |
| 10. ESC9-ESC13 — NEWER DISCOVERIES; 11. CERTIFICATE-BASED PERSISTENCE; 12. AD CS ATTACK DECISION TREE | [Read](./references/02-esc9-esc13-newer-discoveries.md) |
| Advanced: AD CS ESC1–ESC13 Quick Reference Matrix | [Read](./ADCS_ESC_MATRIX.md) |
