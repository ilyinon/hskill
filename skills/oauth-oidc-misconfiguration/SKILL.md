---
name: oauth-oidc-misconfiguration
description: Review OAuth/OIDC redirect registration, callback/session binding, PKCE, nonce, provider identity, and grant scope. Use for federation flow questions; JWT signing and key lookup have a separate playbook.
---

# OAuth and OIDC flow binding

Map authorization request, callback, token exchange, and resulting local/provider identity. Use owned test accounts and compare an accepted same-session baseline with a controlled mismatch. Missing state, nonce, or PKCE is a candidate only under the actual flow and binding model; demonstrate forbidden code acceptance, identity transition, or permission change.

## References

| Current question | Read |
|---|---|
| Login CSRF, code substitution, PKCE, nonce, account linking | [Callback and transaction binding](./references/callback-binding.md) |
| Registered redirect, parser behavior, response destination | [Redirect validation](./references/redirect-validation.md) |
| Implicit/front-channel delivery or grant scope | [Token delivery and scope](./references/token-delivery-scope.md) |
| Applicable checks for an already mapped flow | [Targeted checklist](./references/flow-checklist.md) |

Read only the relevant reference. JWT signature/key/claim mechanics: [JWT validation](../jwt-oauth-token-attacks/SKILL.md), only when that trust question arises. Browser cross-origin reads: [CORS](../cors-cross-origin-misconfiguration/SKILL.md). XML federation: [SAML](../saml-sso-assertion-attacks/SKILL.md). Known flow questions need no category router.
