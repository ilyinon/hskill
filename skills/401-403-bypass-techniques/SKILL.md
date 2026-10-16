---
name: 401-403-bypass-techniques
description: >-
  401/403 bypass playbook. Use when encountering access-denied responses on admin panels, API endpoints, or restricted paths. Covers path manipulation, HTTP method tampering, header injection, protocol downgrade, and automated bypass tools.
---

# 401 403 Bypass Techniques

## Working approach

- Establish the denied protected resource and current principal
- Compare a small path/method/header variant with the same identity and an authorized baseline
- Distinguish proxy handling from application authorization.

## Evidence and limits

Protected data or a forbidden action becomes available to the unchanged unauthenticated or low-privilege principal.

A 200, redirect, HEAD response, generic shell, or allowed OPTIONS response alone is insufficient; mutation methods require permitted test objects.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| Evidence threshold; 1. PATH MANIPULATION BYPASSES; 2. HTTP METHOD BYPASS; 3. HEADER-BASED BYPASS | [Read](./references/01-evidence-threshold.md) |
| 4. PROTOCOL VERSION BYPASS; 5. VERB TAMPERING + PATH COMBINATION; 6. TECHNOLOGY-SPECIFIC BYPASSES; 7. AUTOMATED TOOLS; 8. DECISION TREE; 9. QUICK REFERENCE — KEY PAYLOADS | [Read](./references/02-protocol-version-bypass.md) |
