---
name: mobile-ssl-pinning-bypass
description: >-
  Mobile SSL pinning bypass playbook. Use when intercepting HTTPS traffic from mobile applications that implement certificate pinning, public key pinning, or SPKI hash pinning on Android and iOS, including React Native, Flutter, and Xamarin frameworks.
---

# Mobile Ssl Pinning Bypass

## Working approach

- Identify platform/API version, build type, TLS stack, trust store, and pinning layer
- Establish a working proxy and baseline connection before instrumentation
- Alter one trust decision in the permitted test app and verify actual traffic.

## Evidence and limits

The test setup observes the intended app traffic while documenting exactly which client control was changed.

A connection failure may be proxy, trust-store, QUIC, mTLS, or network configuration; a local pinning bypass does not itself prove a server vulnerability.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SSL PINNING TYPES | [Read](./references/01-ssl-pinning-types.md) |
| 2. ANDROID BYPASS METHODS | [Read](./references/02-android-bypass-methods.md) |
| 3. iOS BYPASS METHODS; 4. FRAMEWORK-SPECIFIC BYPASSES; 5. CERTIFICATE TRANSPARENCY & HPKP | [Read](./references/03-ios-bypass-methods.md) |
| 6. TROUBLESHOOTING; 7. SSL PINNING BYPASS DECISION TREE; 8. PROXY SETUP QUICK REFERENCE | [Read](./references/04-troubleshooting.md) |
