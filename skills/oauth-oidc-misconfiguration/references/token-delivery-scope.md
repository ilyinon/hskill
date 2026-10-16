# OAuth token delivery and scope

Read for front-channel token delivery or a grant/token scope mismatch. Establish the approved grant and resulting resource permissions. For URL, history, or logging exposure, read only the relevant section of [token exposure](../../jwt-oauth-token-attacks/references/token-exposure.md).

## 9. OAUTH — IMPLICIT FLOW TOKEN THEFT

Implicit flow: token sent in URL fragment `#access_token=...`

**Fragment leakage scenarios**:
- A script executing in the token-bearing page can read its own `window.location.href`/`location.hash`. `document.referrer` does not expose the previous page's fragment.
- An open-redirect chain may deliver or inherit a fragment at a forbidden destination, depending on the actual redirect responses. Capture the resulting URL and script access; do not infer it from a proposed URL.

Modern OAuth guidance discourages the implicit grant because of token-delivery risks; classify legacy flows from their demonstrated behavior, not solely their presence. [RFC 9700 section 2.1.2](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.1.2).


## 10. OAUTH — SCOPE ESCALATION

Request broader scope than authorized in authorization code:
```
Authorized scope: read:profile
Attack: During token exchange, add scope=admin or scope=read:admin
→ Does server grant requested scope or issued scope?
```
