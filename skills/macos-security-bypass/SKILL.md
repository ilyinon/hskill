---
name: macos-security-bypass
description: >-
  macOS security bypass playbook. Use when targeting macOS endpoints and need to bypass TCC, Gatekeeper, SIP, sandbox, code signing, or entitlement-based protections during authorized red team or pentest engagements.
---

# Macos Security Bypass

## Working approach

- Identify the exact TCC, Gatekeeper, SIP, sandbox, or signing decision and OS build
- Record attacker access and responsible process identity
- Reproduce the smallest permission change or prohibited access in an isolated test environment.

## Evidence and limits

The identified control permits an action it should deny under the stated identity and policy.

A database row, quarantine change, local admin access, or historical CVE alone is not a universal bypass; account for prompt state and build-specific mitigations.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. TCC (TRANSPARENCY, CONSENT, CONTROL) OVERVIEW; 2. GATEKEEPER BYPASS; 3. SIP (SYSTEM INTEGRITY PROTECTION) | [Read](./references/01-tcc-transparency-consent-control-overview.md) |
| 4. SANDBOX ESCAPE; 5. CODE SIGNING & ENTITLEMENTS; 6. PERSISTENCE AFTER BYPASS; 7. macOS SECURITY BYPASS DECISION TREE; 8. QUICK REFERENCE: TOOL COMMANDS | [Read](./references/02-sandbox-escape.md) |
| Advanced: TCC Bypass Matrix — Per-Version & Per-Protection Techniques | [Read](./TCC_BYPASS_MATRIX.md) |
