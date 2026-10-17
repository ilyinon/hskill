---
name: prototype-pollution-advanced
description: >-
  Advanced prototype pollution playbook — server-side RCE, client-side gadgets, filter bypasses, and detection techniques. Companion to ../prototype-pollution/ for basics. Use when you've confirmed pollution and need to escalate to code execution or find framework-specific gadgets.
---

# Prototype Pollution Advanced

## Working approach

- Start with a demonstrated pollution source and exact library/runtime configuration
- Map own versus inherited properties and reachable gadget reads
- Validate a controlled downstream effect in an isolated instance with state reset.

## Evidence and limits

The demonstrated pollution influences a reachable security-sensitive consumer under the tested version and call context.

A historical gadget catalog or Object.prototype marker is not RCE; Object.assign is not categorically safe, and persistent prototype mutations can contaminate later tests.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SERVER-SIDE PP → RCE; 2. CLIENT-SIDE PROTOTYPE POLLUTION; 3. DETECTION TECHNIQUES | [Read](./references/01-server-side-pp-rce.md) |
| 4. BYPASS `__proto__` FILTERS; 5. EXPLOITATION FLOW; 6. DECISION TREE; 7. QUICK REFERENCE — KEY PAYLOADS | [Read](./references/02-bypass-proto-filters.md) |
| Advanced: Prototype Pollution — Known Gadgets Reference | [Read](./KNOWN_GADGETS.md) |
