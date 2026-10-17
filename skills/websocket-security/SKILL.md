---
name: websocket-security
description: >-
  WebSocket handshake, CSWSH, tooling (wsrepl, ws-harness, Burp), and common flaws. Use when apps use real-time channels, chat, notifications, or WS-backed APIs.
---

# Websocket Security

## Working approach

- Map handshake, Origin/session binding, subprotocols, per-message authorization, and binary formats
- Reproduce a browser connection under realistic cookie rules
- Compare owned identities/topics and validate a controlled message effect.

## Evidence and limits

The unchanged or victim test identity crosses an intended channel, object, origin, or message-authority boundary.

A 101 or accepted Origin alone does not prove CSWSH; WebSocket frames are not arbitrary raw HTTP unless a specific backend/proxy desynchronization exists.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 0. QUICK START; 1. PROTOCOL BASICS; 2. CROSS-SITE WEBSOCKET HIJACKING (CSWSH); 3. TESTING WITH TOOLS; 4. COMMON VULNERABILITIES; 5. DECISION TREE | [Read](./references/01-quick-start.md) |
| 7. CSWSH — STEP-BY-STEP EXPLOITATION; 8. WEBSOCKET SMUGGLING; 9. SOCKET.IO SPECIFIC VULNERABILITIES; 10. WEBSOCKET MESSAGE INJECTION | [Read](./references/02-cswsh-step-by-step-exploitation.md) |
| 11. BINARY WEBSOCKET MESSAGE MANIPULATION | [Read](./references/03-binary-websocket-message-manipulation.md) |
