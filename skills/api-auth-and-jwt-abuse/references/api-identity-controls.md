# API identity, rate limits, and batch candidates

Use when the API consumes proxy identity, client-IP headers, or batch requests. Establish the trusted ingress and endpoint policy first.

## Header and rate-limit candidates

```text
X-Forwarded-For: 1.2.3.4
X-Real-IP: 5.6.7.8
Forwarded: for=9.9.9.9
User-Agent rotation
Path case / slash variants
```

These are candidate dimensions, not automatic bypasses. A trusted ingress can remove client-supplied headers or overwrite them. Compare counter identity, effective principal, successful operation, and a negative control within the authorized request budget.

## Batch candidates

- Arrays of login mutations.
- Bulk object fetches with varying owned-test IDs.
- Repeated reset/verification operations in one permitted batch.

Count actual operations, resulting objects, and per-principal limits; accepting a JSON array does not establish abuse. For schema-specific mechanics, use [GraphQL](../../graphql-and-hidden-parameters/SKILL.md).

## Hidden writable fields

```text
role
isAdmin
admin
verified
plan
tier
permissions
org
owner
```

A field name is a lead. Demonstrate a forbidden persisted or effective state change under a fixed low-privilege identity. Use [API authorization](../../api-authorization-and-bola/SKILL.md) for the full control model.
