---
name: nosql-injection
description: >-
  NoSQL injection playbook. Use when MongoDB-style operators, JSON query objects, flexible search filters, or backend query DSLs may allow data or logic abuse.
---

# Nosql Injection

## Working approach

- Identify database, driver, decoding, query construction, expected types, and reachable operators
- Compare a benign value with a controlled type/operator mutation
- Observe query or authorization semantics before selecting a database-specific technique.

## Evidence and limits

Attacker input changes query structure or interpretation beyond the intended data value and causes a demonstrated effect.

JSON syntax, an error, or a delay alone is insufficient; MongoDB, CouchDB, Redis, and ODM layers have different languages and protections.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPT — OPERATOR INJECTION; 2. MONGODB — LOGIN BYPASS; 3. MONGODB OPERATORS FOR INJECTION; 4. BLIND DATA EXTRACTION VIA $REGEX; 5. MONGODB $WHERE INJECTION (JS EXECUTION); 6. AGGREGATION PIPELINE INJECTION; 7. HTTP PARAMETER POLLUTION FOR NOSQL; 8. COUCHDB ATTACKS; 9. REDIS INJECTION; 10. DETECTION PAYLOADS; 11. NOSQL VS SQL — KEY DIFFERENCES; 12. TESTING CHECKLIST | [Read](./references/01-core-concept-operator-injection.md) |
| 13. BLIND NoSQL EXTRACTION AUTOMATION; 14. AGGREGATION PIPELINE INJECTION | [Read](./references/02-blind-nosql-extraction-automation.md) |
