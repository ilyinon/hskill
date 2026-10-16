---
name: sqli-sql-injection
description: >-
  SQL injection playbook. Use when input reaches SQL queries, authentication logic, sorting, filtering, reporting, or DB-specific blind and out-of-band execution paths.
---

# Sqli Sql Injection

## Working approach

- Trace input to the actual query builder, database, driver, and parameter binding
- Compare a benign baseline with a syntax/semantic control appropriate to that sink
- Establish query-structure control before selecting extraction or escalation details.

## Evidence and limits

Input changes SQL structure or query semantics beyond the intended parameter value with reproducible evidence.

An error, quote reflection, or single delayed response is insufficient; correctly bound values are different from dynamically concatenated identifiers or clauses.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. QUICK START; 1. DETECTION — SUBTLE INDICATORS; 2. DATABASE FINGERPRINTING; 3. UNION-BASED DATA EXTRACTION; 4. BLIND INJECTION — INFERENCE TECHNIQUES | [Read](./references/01-quick-start.md) |
| 5. OUT-OF-BAND (OOB) EXFILTRATION — CRITICAL; 6. ESCALATION — OS COMMAND EXECUTION; 7. SECOND-ORDER INJECTION; 8. PARAMETERIZED QUERY BYPASS SCENARIOS; 9. FILTER EVASION TECHNIQUES; 10. DATABASE METADATA EXTRACTION; 11. STORED PROCEDURE ABUSE; 12. QUICK REFERENCE — INJECTION TEST STRINGS | [Read](./references/02-out-of-band-oob-exfiltration-critical.md) |
| 13. WAF BYPASS MATRIX; 14. WAF BYPASS MATRIX | [Read](./references/03-waf-bypass-matrix.md) |
| Advanced: SQL Injection — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
| Advanced: SQLMap Advanced Workflow & Deep SQL Injection Techniques | [Read](./SQLMAP_ADVANCED.md) |
