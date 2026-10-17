---
name: expression-language-injection
description: >-
  Expression Language injection playbook. Use when Java EL, SpEL, OGNL, or MVEL expressions may evaluate attacker-controlled input in Spring, Struts2, Confluence, or similar frameworks.
---

# Expression Language Injection

## Working approach

- Identify Java framework, expression sink, evaluator mode, and exposed objects
- Compare harmless expression evaluation with literal/error controls
- Select SpEL, OGNL, or EL details only after identifying the engine and configuration.

## Evidence and limits

Server-side evaluation of attacker-controlled expression syntax is demonstrated, with any further impact separately supported.

Arithmetic output alone does not identify the engine or prove RCE; restricted evaluation contexts and patched framework paths can block escalation.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. DETECTION — POLYGLOT PROBES; 2. SpEL (SPRING EXPRESSION LANGUAGE); 3. OGNL (OBJECT-GRAPH NAVIGATION LANGUAGE); 4. JAVA EL (JSP / JSF) | [Read](./references/01-detection-polyglot-probes.md) |
| 5. DETECTION METHODOLOGY; 6. QUICK REFERENCE | [Read](./references/02-detection-methodology.md) |
