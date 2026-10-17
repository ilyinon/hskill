---
name: prototype-pollution
description: >-
  Prototype pollution testing for JavaScript stacks. Use when user input is
  merged into objects (query parsers, JSON bodies, deep assign), when
  configuring libraries via untrusted keys, or when hunting RCE gadgets via
  polluted Object.prototype in Node or the browser.
---

# Prototype Pollution

## Working approach

- Identify the input parser, dynamic property writes, merge implementation, and target object
- Demonstrate a harmless inherited marker in an isolated process
- Trace a reachable gadget separately from the pollution primitive.

## Evidence and limits

Untrusted data changes the relevant prototype/inherited lookup and a claimed downstream effect is independently reproduced.

JSON parsing alone is not pollution; Object.assign can invoke setters and alter the target prototype, while deep pollution and gadget execution are separate claims.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. MECHANISM; 2. CLIENT-SIDE DETECTION; 3. SERVER-SIDE DETECTION (Express / Node, black-box); 4. EXPLOITATION GADGETS; 5. TOOLS; 6. DECISION TREE | [Read](./references/01-quick-start.md) |
| Overview and related routes | [Read](./references/02-overview.md) |
