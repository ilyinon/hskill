---
name: web-cache-deception
description: >-
  Web cache deception and poisoning playbook. Use when CDN, reverse proxy, or application caching may serve sensitive authenticated content to other users due to path confusion or cache key manipulation.
---

# Web Cache Deception

## Working approach

- Identify cache key, routing normalization, cacheability, cookies, and personalized content using unique test keys
- Distinguish deception from poisoning
- Compare a controlled authenticated response with a clean request from a separate test identity.

## Evidence and limits

A clean request receives forbidden cached private content or an attacker-controlled response under the intended shared key.

Reflection, cache headers, or a HIT alone is insufficient; Vary, query policies, separate cache partitions, and origin behavior must agree.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPTS; 2. CACHE DECEPTION — ATTACK METHODOLOGY; 3. CACHE POISONING — ATTACK METHODOLOGY; 4. PATH NORMALIZATION DIFFERENCES; 5. CACHE POISONING REAL-WORLD PATTERN; 6. DEFENSE; 6. TESTING CHECKLIST | [Read](./references/01-core-concepts.md) |
| Advanced: Web Cache Poisoning Techniques — Advanced Reference | [Read](./CACHE_POISONING_TECHNIQUES.md) |
