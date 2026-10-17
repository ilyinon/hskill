---
name: http2-specific-attacks
description: >-
  HTTP/2 protocol-specific attack playbook. Use when the target supports HTTP/2 and you need to exploit binary framing, HPACK compression, h2c upgrade smuggling, pseudo-header injection, stream multiplexing abuse, or H2→H1 downgrade translation flaws.
---

# Http2 Specific Attacks

## Working approach

- Pin negotiated protocol, front/back topology, downgrade behavior, and implementation
- Identify framing, authority, multiplexing, or resource-accounting hypotheses
- Use an isolated connection and bounded requests to distinguish normal protocol rejection from desynchronization.

## Evidence and limits

A controlled second request or response demonstrates the claimed parser or routing boundary failure.

H2 support, an odd error, HPACK use, or a timeout alone does not prove smuggling; avoid shared-user response contamination and unbounded stream tests.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. HTTP/2 ATTACK SURFACE OVERVIEW; 2. h2c (HTTP/2 CLEARTEXT) SMUGGLING; 3. PSEUDO-HEADER INJECTION; 4. HPACK COMPRESSION ATTACKS | [Read](./references/01-http-2-attack-surface-overview.md) |
| 5. STREAM MULTIPLEXING ABUSE; 6. HTTP/2 → HTTP/1.1 DOWNGRADE ISSUES; 7. SERVER PUSH CACHE POISONING; 8. DECISION TREE; 9. TOOLS REFERENCE; 10. QUICK REFERENCE | [Read](./references/02-stream-multiplexing-abuse.md) |
