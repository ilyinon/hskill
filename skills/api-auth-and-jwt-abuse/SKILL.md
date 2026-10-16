---
name: api-auth-and-jwt-abuse
description: Review API-key and bearer credential extraction, proxy identity headers, endpoint authentication consistency, and rate-limit boundaries. Use JWT validation directly for signing/key/claim questions, and OAuth/OIDC for federation flows.
---

# API authentication boundary

- Identify how the endpoint extracts credentials and maps them to a principal, tenant, scopes, and permissions.
- Compare the same operation with a valid baseline, missing/invalid credentials, and one controlled header or endpoint variant. Keep the principal fixed for authorization checks.
- For forwarded identity or client IP, trace trusted proxy hops, header stripping, and which value the application actually consumes.
- Test rate-limit behavior only within the permitted request budget. A different header or response status does not prove a bypass; show the protected action and counter behavior.

## Evidence and limits

Confirm an authentication flaw when a request outside the credential/identity policy gains a protected capability. Record the resulting principal and permissions. Batch execution, token decoding, or an accepted forwarded header alone is insufficient.

## References

| Current need | Read |
|---|---|
| Header, rate-limit, or batch candidates | [API-specific candidates](./references/api-identity-controls.md) |
| JWT signing, key trust, or claims | [JWT validation](../jwt-oauth-token-attacks/SKILL.md) |
| OAuth/OIDC callback or account binding | [OAuth/OIDC](../oauth-oidc-misconfiguration/SKILL.md) |
| Hidden writable fields or object permissions | [API authorization](../api-authorization-and-bola/SKILL.md) |
| GraphQL batching and hidden parameters | [GraphQL](../graphql-and-hidden-parameters/SKILL.md) |
| Login/reset/default-credential workflow | [Authentication](../authbypass-authentication-flaws/SKILL.md) |
