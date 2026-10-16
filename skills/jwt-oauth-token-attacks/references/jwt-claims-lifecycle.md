# JWT claims, audience, and lifecycle

Read after signature policy is understood. Establish the expected issuer, audience, token kind, subject mapping, expiration/leeway, and revocation model. A refresh token and an access token need different validation rules. Logout does not universally revoke every issued access token; compare the documented session policy.

Use an accepted baseline and single mutations, including validly signed wrong-audience/issuer controls when authorized. Decoded or modified claims prove nothing unless the verifier accepts them with a forbidden capability. [RFC 8725 sections 3.8–3.12](https://www.rfc-editor.org/rfc/rfc8725.html).

## 12. JWT TESTING CHECKLIST

```
□ Decode header + payload (base64 decode each part)
□ Identify algorithm: HS256/RS256/ES256/none
□ Modify payload fields (role, userId, isAdmin) → change signature too
□ Test alg:none → remove signature entirely
□ If RS256: find public key → attempt RS256→HS256 confusion
□ If HS256: brute force with hashcat/rockyou
□ Check kid parameter → try SQL injection + path traversal
□ Check jku/x5u header → redirect to attacker JWKS
□ Test token reuse after logout
□ Test expired token acceptance (exp claim)
□ Check for token in GET params (log leakage) vs header
```
