---
name: orm-search-injection
description: >-
  Search-parameter and query-builder injection into LIKE predicates. Use when
  filter parameters (Ransack q[attr_cont], legacy attr_start keys, JPA/Sequelize
  like, raw LIKE) reach the database unescaped and searchable columns may hold
  sensitive values. Covers wildcard-oracle confirmation, blind per-character
  extraction of digests, and the controls that separate a real oracle from noise.
---

# ORM Search Injection (LIKE wildcard oracle)

## Working approach

- Identify the search layer and its predicates from observed parameters: Ransack
  `q[attr_cont]` / `q[attr_start]` / `q[attr_end]`, legacy top-level `?attr_cont=`,
  Sequelize `Op.like`, JPA/Hibernate `like`, hand-written `LIKE '%…%'`. Record which
  columns the app admits to search (Ransack `ransackable_attributes`, serializer
  allowlists, or leaked source).
- Prove wildcard pass-through before any extraction: a benign term (baseline), a
  pattern that must match a known-public value (positive control), and a random
  same-length prefix (negative control). Value-side `%`/`_` that changes the result
  set is the oracle; a quote or DB error instead means structure-level SQLi — switch
  to [sqli-sql-injection](../sqli-sql-injection/SKILL.md).
- Chain the prerequisites as separate observations: (1) attacker-controlled
  predicate, (2) sensitive column searchable through the allowlist (a digest/token
  column reachable is the finding), (3) storable value is matchable (fixed-format
  hex, prefix-ordered). A search parameter alone proves none of them.

## Evidence and limits

- A matching prefix is an observation, not impact. A recovered digest is a
  credential only after offline cracking plus a login, platform verdict, or
  equivalent confirmation.
- Distinguish "predicate ignored" from "no match": ignored predicates return the
  unfiltered baseline, so compare against both an unfiltered request and a
  known-false pattern on a public column.
- Check case sensitivity on the first two probes. `_cont` may compile to ILIKE
  (PostgreSQL) or a case-insensitive-collation LIKE (MySQL default); this decides
  whether one hex alphabet suffices.
- Do not label this SQL injection: values stay bound; only LIKE metacharacters
  cross the boundary. Claim the stronger class only with structure control.

## Solving decisions

When a probe result is ambiguous, choose the next discriminating check in
[diagnostics](./references/diagnostics.md). For a complete extraction with controls
and a checked result, read the [worked case](./references/worked-cases.md).

## References

| Current need | Read selectively |
|---|---|
| Predicate matrix, per-character extraction loop, request budget, remediation checks | [Oracle extraction](./references/oracle-extraction.md) |
| Ambiguous responses, ignored parameters, rate limits | [Diagnostics](./references/diagnostics.md) |
| Digest extraction from a users-search endpoint | [Worked case](./references/worked-cases.md) |
