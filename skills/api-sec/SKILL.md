---
name: api-sec
description: Route an ambiguous API assessment between surface discovery, object permissions, API credentials, JWT trust, and GraphQL. Use a known specialty directly.
---

# API Security Router

This is the routing entry point for API security testing.

When the boundary is unclear, use this optional router to decide whether the API issue is mostly recon/docs, object authorization, token trust, or GraphQL/hidden parameters, then route to a deeper topic skill.

## When to Use

- The target exposes REST APIs, mobile backends, or GraphQL endpoints
- You need to define API testing order before going into specific topics
- You want to handle object authorization, JWT, GraphQL, and hidden fields as separate tracks

## Skill Map

- [API Recon and Docs](../api-recon-and-docs/SKILL.md): OpenAPI, Swagger, version drift, hidden documentation
- [API Authorization and BOLA](../api-authorization-and-bola/SKILL.md): BOLA, BFLA, method abuse, hidden writable fields
- [API Auth and JWT Abuse](../api-auth-and-jwt-abuse/SKILL.md): bearer token, header trust, claim abuse, rate-limit bypass
- [GraphQL and Hidden Parameters](../graphql-and-hidden-parameters/SKILL.md): introspection, batching, undocumented fields, hidden parameters

## Quick Triage

| Observation | Route |
|---|---|
| Swagger or OpenAPI is present | [api-recon-and-docs](../api-recon-and-docs/SKILL.md) |
| IDs appear in URL, JSON, headers, or GraphQL args | [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) |
| JWT signature, algorithm, key, or claim policy | [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) |
| API key, credential extraction, proxy identity, or rate-limit boundary | [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) |
| OAuth/OIDC callback or account binding | [oauth-oidc-misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) |
| `/graphql` or batched JSON arrays are present | [graphql-and-hidden-parameters](../graphql-and-hidden-parameters/SKILL.md) |
| Registration, login, or profile updates accept extra fields | [api-authorization-and-bola](../api-authorization-and-bola/SKILL.md) then [api-auth-and-jwt-abuse](../api-auth-and-jwt-abuse/SKILL.md) |

## Broad-assessment flow

Use this sequence only for a requested broad review; known topics can skip it.

1. Start with exposed endpoints and documentation assets
2. Then evaluate object-level and function-level authorization
3. Then evaluate token, header, signature, and rate-limit boundaries
4. If GraphQL or complex JSON is present, continue with hidden fields and schema abuse

## Related Categories

- [auth-sec](../auth-sec/SKILL.md)
- [business-logic-vuln](../business-logic-vuln/SKILL.md)
- [recon-for-sec](../recon-for-sec/SKILL.md)
