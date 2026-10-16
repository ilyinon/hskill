# authbypass-authentication-flaws technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. MULTI-FACTOR AUTHENTICATION BYPASS

### Session Cookie Before 2FA Completion
```
Flow: Login (password correct) → redirect to 2FA page → enter code
Attack: After password step, session cookie is set but 2FA not yet checked.
→ Use session cookie to directly access /dashboard
→ Skip 2FA page entirely
```

### 2FA Code Brute Force
```
4-6 digit TOTP codes = 1,000,000 possibilities max
If no lockout on 2FA step:
→ Brute force all codes (tool: Burp Intruder, sequential)
→ TOTP windows: 30-second window, some accept previous/next window
```

### 2FA on Critical Actions Not On Login
```
Login doesn't require 2FA, but:
DELETE /account or POST /transfer requires 2FA
Attack: Is 2FA checked on those actions or only on login?
→ If only login: log in once → no 2FA needing verification for actions
```

### 2FA Backup Code Abuse
```
Generate backup codes (usually 8-10 single-use)
Test: 
→ Are backup codes rate-limited?
→ Can backup codes be used multiple times?
→ Short codes (6-8 chars)? Brute-force if no rate limit
```

### 2FA Code Reuse
```
TOTP codes valid for one use
→ Use same TOTP code twice → does second use work?
→ Replay attack if server doesn't track used codes
```

---

## 6. OAUTH / SSO ACCOUNT TAKEOVER PATTERNS

### Email Claim Trust
```
1. Create account at attacker-controlled OAuth provider
2. Set email claim = victim@target.com
3. Link/login via that provider
→ If server trusts email claim without verification → account merge/takeover
```

### Password Doesn't Apply After SSO Link
```
1. User links Google SSO
2. User forgets password (account has no password set after SSO only)
3. "Forgot Password" flow → resets password even for SSO-only accounts?  
→ Can set password → now bypass SSO → direct login
```

---

## 7. USERNAME / PASSWORD FIELD MANIPULATION

### Long Password DoS → Bypass
```
Some apps hash passwords before sending to database.
bcrypt has 72-byte limit — input beyond 72 bytes is ignored.
Attack: 
→ Register with password "A"*100
→ Login with password "A"*72 → same hash → works
→ Login with "A"*71 + "totally different" → if truncation → same hash if first 72 chars match
```

### Null Byte in Username
```
username=admin%00 vs username=admin
→ Null byte truncation in some string comparisons
→ "admin\0attacker" = "admin" in C-string comparison
```

### Unicode Normalization
```
Username: "ⓢcott" → normalizes to "scott" → impersonates "scott"
Username: "admin" (various Unicode homoglyphs for letters a,d,m,i,n)
```

---

## 8. SESSION MANAGEMENT FLAWS

### Session Not Invalidated on Logout
```
1. Log in → capture session cookie
2. Log out
3. Replay captured session cookie → still valid?
→ Session not server-side invalidated
```

### Session Not Regenerated on Privilege Change
```
1. Log in as low priv → get session cookie
2. Admin upgrades your role
3. Old session cookie now has admin access?
→ Session not regenerated → old token inherits new privileges
```

### Predictable Session Tokens
```
Token: base64(userid+timestamp) → reversible
Token: sequential integers → session ID= your_session_id -/+ small number
Token: short random (32-bit entropy) → brute-forceable
```

---

## 9. AUTHENTICATION TESTING CHECKLIST

```
□ Try SQL injection on login fields (' OR 1=1--)
□ Test password reset: predict token, host header injection, Referer leak
□ Test account enumeration via error messages / timing
□ Check 2FA: skip step (direct URL), brute force codes, reuse codes
□ Test brute force protections: X-Forwarded-For bypass, reverse brute
□ Check session invalidation on logout
□ Check session regeneration after privilege change
□ Test password change requiring current password  
□ Test long passwords (bcrypt 72-byte truncation)
□ OAuth/SSO: test email claim trust, password set after SSO
□ Check remember_me tokens: how long, revocable, predictable?
```

---

## 10. PASSWORD RESET ATTACK MATRIX (22 Patterns)

| # | Pattern | Description |
|---|---|---|
| 1 | Predictable reset token | Token based on timestamp, user ID, or sequential number |
| 2 | Token not bound to user | Use token generated for user A to reset user B |
| 3 | Token in response body | Reset token returned in HTTP response (not just email) |
| 4 | Token in URL parameter | Reset link token visible in Referer header to external resources |
| 5 | No token expiration | Token remains valid indefinitely |
| 6 | Token reuse | Same token works multiple times |
| 7 | Short/brute-forceable token | 4-6 digit numeric code without rate limiting |
| 8 | Password reset via host header | `Host: attacker.com` → reset link sent with attacker's domain |
| 9 | Registration overwrites existing account | Register with same email → overwrites password |
| 10 | Step skip (frontend only) | Jump directly to "set new password" step via URL |
| 11 | Response manipulation | Change `{"status":"fail"}` to `{"status":"success"}` in proxy |
| 12 | Verification code in response | SMS/email code returned in API response |
| 13 | Parallel session reset | Start reset for A, complete with B's session |
| 14 | Email/phone parameter pollution | `email=victim@x.com&email=attacker@x.com` |
| 15 | Unicode normalization | `admin@target.com` vs `ADMIN@target.com` vs Unicode confusables |
| 16 | SQL injection in reset | Email field injectable in reset query |
| 17 | IDOR on reset endpoint | Change user ID in reset confirmation request |
| 18 | Cross-protocol reset | Mobile API doesn't validate same token as web |
| 19 | Default security questions | Guessable answers, no rate limit |
| 20 | Token generation race condition | Multiple simultaneous requests generate same token |
| 21 | Logout doesn't invalidate reset | After password change, old sessions still work |
| 22 | Reset link cached by CDN/proxy | Public cache stores reset link with token |

---

