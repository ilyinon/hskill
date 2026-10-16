---
name: ntlm-relay-coercion
description: >-
  NTLM relay and authentication coercion playbook. Use when capturing and relaying NTLM authentication to escalate privileges via SMB, LDAP, HTTP, or MSSQL relay targets, combined with PetitPotam, PrinterBug, and other coercion methods.
---

# Ntlm Relay Coercion

## Working approach

- Identify the coercing service, originating identity, target protocol, signing, channel binding, EPA, and required permissions
- Distinguish credential capture, coercion, relay acceptance, and authorization
- Verify only the permitted test capability.

## Evidence and limits

A relayed authentication is accepted by the target service and grants a capability forbidden by the intended trust boundary.

A captured NTLM exchange or successful coercion is not successful relay; signing and binding checks may block the target while valid credential-based access remains possible.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. NTLM RELAY FUNDAMENTALS; 2. RELAY TARGET MATRIX; 3. RESPONDER — CREDENTIAL CAPTURE; 4. NTLMRELAYX — RELAY EXECUTION; 5. MITM6 — IPv6 DNS TAKEOVER | [Read](./references/01-ntlm-relay-fundamentals.md) |
| 6. CROSS-PROTOCOL RELAY; 7. WEBDAV-BASED COERCION; 8. NTLM RELAY DECISION TREE | [Read](./references/02-cross-protocol-relay.md) |
| Advanced: Authentication Coercion Methods | [Read](./COERCION_METHODS.md) |
