---
name: http-parameter-pollution
description: >-
  HTTP Parameter Pollution (HPP): duplicate query/body keys parsed differently by servers, proxies, WAFs, and app frameworks. Use when filters and application layers disagree on which value wins, enabling bypass, SSRF second URL, logic abuse, or CSRF token confusion.
---

# Http Parameter Pollution

## Working approach

- Determine how each proxy, framework, parser, and binding layer handles duplicate keys
- Compare first/last/array/concatenation behavior using harmless distinct markers
- Identify the security decision and the consumer that disagree.

## Evidence and limits

The same request is checked using one value but used for a protected action with another interpretation.

Duplicate keys or an array response alone are not a flaw; behavior depends on parser, middleware, content type, and API binding, not just server brand.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. SERVER BEHAVIOR MATRIX; 2. PAYLOAD PATTERNS; 3. ATTACK SCENARIOS; 4. TOOLS; 5. DECISION TREE | [Read](./references/01-quick-start.md) |
