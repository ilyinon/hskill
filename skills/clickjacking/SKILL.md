---
name: clickjacking
description: >-
  Clickjacking playbook. Use when testing whether target pages can be framed, whether X-Frame-Options or CSP frame-ancestors are properly configured, and whether UI redress attacks can trigger sensitive actions.
---

# Clickjacking

## Working approach

Inspect every effective ancestor restriction and the actual browser/session action path. Use a harmless owned setting or marker for any permitted interaction proof.

## Evidence and limits

Frameability is a prerequisite. Confirm the meaningful state change under realistic session, interaction and reauthentication conditions before claiming its impact.

## References

- For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md).
- For a complete change of approach and independent controls, read the [worked case](./references/worked-cases.md).
- For matching recipes, tools and detailed variants, read the relevant section of the [technical playbook](./references/legacy-playbook.md). Establish its actual parser, runtime or workflow prerequisites first.
