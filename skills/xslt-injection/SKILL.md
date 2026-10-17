---
name: xslt-injection
description: >-
  XSLT injection testing: processor fingerprinting, XXE and document() SSRF, EXSLT write primitives, PHP/Java/.NET extension RCE surfaces. Use when user-controlled XSLT/stylesheet input or transform endpoints are in scope.
---

# Xslt Injection

## Working approach

- Confirm that controlled stylesheet logic is compiled/executed and fingerprint processor/configuration
- Separate XML entity parsing, document loading, output writing, and extension functions
- Choose one harmless marker effect supported by that engine.

## Evidence and limits

The transform performs the claimed read, fetch, write, or extension action outside intended policy.

A stylesheet accepted as data or a vendor string is not RCE; secure processing, resolvers, extension permissions, and XML well-formedness constrain each path.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. VENDOR DETECTION; 2. EXTERNAL ENTITY (XXE VIA XSLT); 3. FILE READ VIA `document()`; 4. FILE WRITE VIA EXSLT (`exslt:document`); 5. RCE VIA PHP (`php:function`) | [Read](./references/01-quick-start.md) |
| 6. RCE VIA JAVA (SAXON / XALAN EXTENSIONS); 7. RCE VIA .NET (`msxsl:script`); 8. DECISION TREE; Payloads All The Things (PAT) Note; Tooling (practical); Related | [Read](./references/02-rce-via-java-saxon-xalan-extensions.md) |
