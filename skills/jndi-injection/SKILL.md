---
name: jndi-injection
description: >-
  JNDI injection playbook. Use when Java applications perform JNDI lookups with attacker-controlled names, especially via Log4j2, Spring, or any code path reaching InitialContext.lookup().
---

# Jndi Injection

## Working approach

- Identify the lookup sink, attacker-controlled name, JDK build, provider, and local classpath
- Distinguish outbound lookup from object reconstruction and code execution
- Verify each milestone with a controlled callback or local reproduction.

## Evidence and limits

The exact lookup or reconstruction boundary is demonstrated, with execution claimed only when separately observed.

A DNS/LDAP callback is not RCE; remote-codebase defaults, factory changes, filters, and available classes are version-dependent.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE MECHANISM; 2. ATTACK VECTORS; 3. JDK VERSION CONSTRAINTS AND BYPASS; 4. TOOLING; 5. LOG4J2 — CVE-2021-44228 (LOG4SHELL) | [Read](./references/01-core-mechanism.md) |
| 6. OTHER JNDI SINKS (BEYOND LOG4J); 7. TESTING METHODOLOGY; 8. QUICK REFERENCE | [Read](./references/02-other-jndi-sinks-beyond-log4j.md) |
