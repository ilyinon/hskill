# OAuth callback, PKCE, and OIDC binding

Read for login CSRF, code substitution, account linking, and transaction binding. Inspect client ID, redirect URI, one-time code consumption, session-held verifier, S256 enforcement, and provider identity. For OIDC, validate nonce where required by the flow and the ID-token issuer/audience/signature. Never treat a decoded ID token as identity proof.

Status and limits: see the named record in the [verification registry](../../hack/verification.json). Record: `oauth-callback-binding`.

<a id="7-oauth-20--state-parameter-missing-csrf"></a>

## 7. OAUTH 2.0 — CALLBACK BINDING WHEN STATE IS ABSENT

Check request-to-session binding across the complete flow. A missing `state` is not sufficient proof when a correctly implemented, transaction-bound PKCE or applicable OIDC nonce mechanism supplies CSRF protection. Verify those prerequisites rather than deleting a parameter and declaring takeover. [RFC 9700 section 2.1](https://www.rfc-editor.org/rfc/rfc9700.html#section-2.1).

```
Attack:
1. Click "Login with Google" → OAuth starts → intercept the redirect URL:
   https://accounts.google.com/oauth2/auth?client_id=APP_ID&redirect_uri=https://target.com/callback&state=MISSING_OR_PREDICTABLE

2. Complete authorization with an owned test account; capture its callback code before exchange
3. Craft URL: https://target.com/oauth/callback?code=ATTACKER_CODE
4. In the second owned test session, observe whether the foreign code is accepted
5. Record the resulting local/provider identity and any forbidden binding
→ A proven login-CSRF/account-binding result; account takeover needs separate impact evidence
```
