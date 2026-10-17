---
name: auth-sec
description: Route an ambiguous authentication, authorization, browser-trust, or federation question to its specialty. Known JWT, OAuth/OIDC, BOLA, CORS, and CSRF questions can use the matching topic directly.
---

# Authentication and Authorization Router

Use this optional router when the relevant authentication or authorization boundary is unclear. A known topic can go directly to its specialty.

Use it to decide whether the issue is mainly login mechanics, object-level authorization, browser trust boundaries, or identity protocols such as OAuth/JWT/SAML before going deeper.

## When to Use

- The target includes login, registration, password reset, 2FA, sessions, JWT, OAuth, or SSO
- You suspect object authorization flaws, cross-tenant access, cross-origin reads, CSRF, or protocol misconfiguration
- You need to decide whether to test authentication or authorization first

## Skill Map

- [Authentication Bypass](../authbypass-authentication-flaws/SKILL.md): login bypass, password reset, 2FA, enumeration, brute-force protections
- [IDOR Broken Object Authorization](../idor-broken-object-authorization/SKILL.md): IDOR, BOLA, BFLA, missing object permissions
- [JWT validation](../jwt-oauth-token-attacks/SKILL.md): signature/algorithm policy, key lookup, claims, token lifecycle
- [OAuth OIDC Misconfiguration](../oauth-oidc-misconfiguration/SKILL.md): redirect URI, state, nonce, PKCE, account binding
- [CSRF Cross Site Request Forgery](../csrf-cross-site-request-forgery/SKILL.md): CSRF tokens, SameSite, JSON CSRF, login CSRF
- [CORS Cross Origin Misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md): reflected Origin, credentialed cross-origin reads, allowlist bypass
- [SAML SSO Assertion Attacks](../saml-sso-assertion-attacks/SKILL.md): assertion wrapping, signature validation, audience, ACS boundaries

## Broad-assessment flow

Use this sequence only for a requested broad review; a narrow question does not require earlier stages.

1. First confirm the authentication model and session boundaries
2. Then confirm object-level and function-level authorization
3. Then move to token, cross-origin, and protocol details
4. If enterprise federation exists, continue with OAuth, OIDC, or SAML topics

## Related Categories

- [api-sec](../api-sec/SKILL.md)
- Default credentials, username variants, wordlist sizing, and port focus are consolidated in [authbypass-authentication-flaws](../authbypass-authentication-flaws/SKILL.md)

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.
