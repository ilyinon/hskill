---
name: active-directory-acl-abuse
description: >-
  Active Directory ACL abuse playbook. Use when exploiting misconfigured AD permissions including GenericAll, WriteDACL, DCSync rights, shadow credentials, LAPS reading, GPO abuse, and BloodHound-guided attack paths.
---

# Active Directory Acl Abuse

## Working approach

- Identify the principal, target object, effective ACEs, inheritance, and ownership
- Choose the specific object right rather than a generic administrator path
- Verify prerequisites and the resulting permission in an authorized lab or permitted read-only view.

## Evidence and limits

An effective permission path connects the starting identity to a previously unavailable object capability.

BloodHound edges and group names are hypotheses until effective permissions and target conditions agree; directory writes need explicit scope and rollback.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. BLOODHOUND ENUMERATION; 2. DANGEROUS ACE TYPES; 3. ACE-SPECIFIC EXPLOITATION; 4. DCSYNC ATTACK | [Read](./references/01-bloodhound-enumeration.md) |
| 5. SHADOW CREDENTIALS; 6. LAPS PASSWORD READING; 7. GPO ABUSE; 8. ACL ATTACK DECISION TREE | [Read](./references/02-shadow-credentials.md) |
| Advanced: BloodHound Attack Paths & Cypher Queries | [Read](./BLOODHOUND_PATHS.md) |
