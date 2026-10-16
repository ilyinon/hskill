---
name: jwt-oauth-token-attacks
description: Validate JWT signatures, algorithm and key trust, claims, and token lifecycle. For OAuth/OIDC callback or account binding, use oauth-oidc-misconfiguration directly.
---

# JWT trust and validation

Map token type, configured algorithm/key source, issuer/audience, and resulting principal. Compare an accepted baseline with one controlled mutation and inspect effective permissions. Decoding, changing an unsigned claim, or possessing another valid token is not forgery.

## References

Read only the reference matching the current question.

| Current question | Read |
|---|---|
| What token structure or claims are present? | [Format and decoding](./references/jwt-format.md) |
| Unsigned acceptance, algorithm confusion, weak HMAC key | [Signature policy](./references/jwt-signature-policy.md) |
| Key lookup or remote key trust: `kid`, `jku`, `x5u` | [Key selection](./references/jwt-key-selection.md) |
| Issuer, audience, token kind, expiration, revocation | [Claims and lifecycle](./references/jwt-claims-lifecycle.md) |
| URL, script, history, or logging exposure | [Token exposure](./references/token-exposure.md) |

OAuth/OIDC redirects, PKCE, nonce, and account linking belong to [OAuth/OIDC](../oauth-oidc-misconfiguration/SKILL.md). API-key or proxy-header identity belongs to [API authentication](../api-auth-and-jwt-abuse/SKILL.md). A known JWT question needs no category router.

Legacy section indexes remain available for existing links: [sections 1–7](./references/01-jwt-anatomy.md), [sections 8–13](./references/02-oauth-redirect-uri-bypass.md).
