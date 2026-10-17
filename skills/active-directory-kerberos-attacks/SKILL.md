---
name: active-directory-kerberos-attacks
description: >-
  Kerberos attack playbook for Active Directory. Use when targeting AD authentication via AS-REP roasting, Kerberoasting, golden/silver/diamond tickets, delegation abuse, or pass-the-ticket attacks.
---

# Active Directory Kerberos Attacks

## Working approach

- Record domain, principal, ticket type, encryption, SPNs, delegation settings, and trust boundary
- Select roasting, delegation, or ticket analysis from those facts
- Check ticket acceptance and the resulting identity separately.

## Evidence and limits

A permitted test demonstrates the claimed credential, ticket, delegation, or service-access boundary.

Obtaining a hash or ticket is not proof of plaintext recovery or domain control; key material, account privileges, policy, and patch state matter.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. KERBEROS AUTHENTICATION PRIMER; 2. AS-REP ROASTING; 3. KERBEROASTING; 4. TICKET FORGING — GOLDEN, SILVER, DIAMOND, SAPPHIRE | [Read](./references/01-kerberos-authentication-primer.md) |
| 5. DELEGATION ATTACKS; 6. PASS-THE-TICKET & OVERPASS-THE-HASH; 7. KERBEROS DOUBLE HOP PROBLEM; 8. KERBEROS ATTACK DECISION TREE | [Read](./references/02-delegation-attacks.md) |
| Advanced: Kerberos Multi-Step Attack Chains | [Read](./KERBEROS_ATTACK_CHAINS.md) |
