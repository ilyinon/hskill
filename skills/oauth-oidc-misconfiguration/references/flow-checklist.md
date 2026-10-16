# OAuth and OIDC targeted checklist

Use only the checks applicable to the observed flow. For the mechanics and evidence threshold, select callback binding, redirect validation, or token delivery from the entry index.

## 13. OAUTH TESTING CHECKLIST

```
□ Check for state parameter in authorization request
□ Test redirect_uri manipulation (open redirect, prefix match, path confusion)
□ Authorization code: verify one-time redemption; evaluate refresh-token rotation under its separate profile
□ Test scope escalation during token exchange
□ Implicit flow: check history/script exposure; fragments are excluded from Referer
□ PKCE: can code_challenge be bypassed or code_verifier be empty?
□ Check for authorization code reuse (code must be single-use)
□ Test account linking abuse: link OAuth to existing account with same email
□ Check OAuth provider confusion: use Apple ID to link where Google expected
```
