---
name: http-host-header-attacks
description: >-
  HTTP Host header injection and routing abuse playbook. Use when the application
  trusts the Host header for generating URLs, routing requests, or access control
  — enabling password reset poisoning, web cache poisoning, SSRF via routing,
  and virtual host bypass.
---

# Http Host Header Attacks

## Working approach

- Record proxy chain, accepted authority forms, trusted forwarding headers, and absolute URL generation
- Vary one host input with a unique benign marker
- Follow the marker to a reset link, cache entry, routing decision, or server fetch.

## Evidence and limits

An untrusted authority changes a protected downstream destination or content with demonstrated impact.

Host reflection, a default vhost, or an error alone is insufficient; reset delivery, cache keys, origin reachability, and proxy trust must be verified.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ATTACK SURFACE; 2. PASSWORD RESET POISONING; 3. WEB CACHE POISONING VIA HOST; 4. SSRF VIA HOST ROUTING; 5. VIRTUAL HOST BYPASS; 6. BYPASS TECHNIQUES WHEN HOST IS VALIDATED | [Read](./references/01-attack-surface.md) |
| 7. FRAMEWORK-SPECIFIC BEHAVIOR; 8. CONNECTION-STATE ATTACKS; 9. HOST HEADER ATTACK DECISION TREE; 10. TRICK NOTES — WHAT AI MODELS MISS | [Read](./references/02-framework-specific-behavior.md) |
