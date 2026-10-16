---
name: request-smuggling
description: >-
  HTTP request smuggling and desynchronization testing. Use when front proxies,
  CDNs, or load balancers disagree with the origin on message framing
  (Content-Length vs Transfer-Encoding), on HTTP/2→HTTP/1 translation, or when
  exploring client-side desync via browser fetch pipelines.
---

# Request Smuggling

## Working approach

- Identify front/back parsers, protocol translation, connection reuse, and framing ambiguity
- Use isolated test connections and a benign follow-up request
- Verify request boundaries and response association with controls.

## Evidence and limits

A controlled request is parsed or routed across the intended boundary differently by the connected components.

A timeout, 400/500, or Content-Length/Transfer-Encoding conflict alone is not desynchronization; avoid shared-user connection contamination.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. QUICK START; 1. CORE CONCEPT; 2. CL.TE VULNERABILITIES; 3. TE.CL VULNERABILITIES | [Read](./references/01-quick-start.md) |
| 4. TE.TE VULNERABILITIES; 5. HTTP/2 REQUEST SMUGGLING; 6. CLIENT-SIDE DESYNC; 7. TOOLS; 8. DETECTION DECISION TREE | [Read](./references/02-te-te-vulnerabilities.md) |
| Advanced: HTTP/2 Smuggling Variants & Advanced Desync Techniques | [Read](./H2_SMUGGLING_VARIANTS.md) |
