---
name: attack-surface-mapping
description: >-
  Draw a testable attack surface from one authorized target URL or one
  application. Use when the user says 攻击面, 供给面, 画攻击面, map the surface,
  application recon, find the business host, JS inventory, or when the only
  visible page is login. Derive hosts, APIs, keys, and the object graph from
  what the app already exposes. Do not open with directory brute or payload
  spray. Use when the user runs /attack-surface-mapping.
---

# Attack Surface Mapping

## Working approach

- Build the product/object/role model from supplied source or captured traffic
- Inventory hosts, methods, auth state, parameter keys, identifiers, transforms, and linked resources with provenance
- Classify responses and hand the most plausible boundary to one topic.

## Evidence and limits

A reproducible inventory ties real entry points to identities, business objects, trust boundaries, and explicit coverage gaps.

Discovery is not permission to probe another host; an empty list, error, or login shell has different meaning and does not establish security.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| When; What must exist (not a file tree) | [Read](./references/01-when.md) |
| Fast path | [Read](./references/02-fast-path.md) |
| Handoff; Anti-patterns | [Read](./references/03-handoff.md) |
| Advanced: Surface Patterns | [Read](./SURFACE_PATTERNS.md) |
