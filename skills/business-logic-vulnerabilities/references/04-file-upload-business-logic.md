# business-logic-vulnerabilities technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 8. FILE UPLOAD BUSINESS LOGIC

For the full upload attack workflow beyond pure logic flaws, also load:

- [upload insecure files](../../upload-insecure-files/SKILL.md)

```
Upload size limit: 10MB
→ Upload 10MB → compress client-side → server decompresses → bomb?
(Zip bomb: 1KB zip → 1GB file = denial of service)

Upload type restriction:
→ Upload .csv for "data import" → inject formulas: =SYSTEM("calc")
  (CSV injection in Excel macro context)
→ Upload avatar → server converts → attack converter (ImageMagick, FFmpeg CVEs)

Storage path prediction:
→ /uploads/USER_ID/filename
→ Can you overwrite other user's file by knowing their ID + filename?
```

---

## 9. TESTING APPROACH

```
For each business process:
1. Map the INTENDED flow (happy path)
2. Ask: "What if I skip step N?"
3. Ask: "What if I send negative/zero/MAX values?"
4. Ask: "What if I repeat this step twice?" (idempotency)
5. Ask: "What happens if I do A then B instead of B then A?"
6. Ask: "What if two users do this simultaneously?"
7. Ask: "Can I modify the 'trusted' status fields?"
8. Think from financial/resource impact angle → highest bounty
```

For the formal 5-phase workflow — Business Modeling → State Machine → Attack-Surface Matrix → Checklist-Driven Testing → Human Judgement — load **[METHODOLOGY.md](../METHODOLOGY.md)**. It includes a single-page decision tree (`Q1 ~ Q7`) for "I'm staring at a request and don't know what to try first".

---

## 10. HIGH-IMPACT CHECKLISTS

For the full per-module list (login / register / password recovery / payment / coupon / order / IDOR / privacy / VIP / URL redirect / cookie & token / race / comments) with `why` and `verify` columns — load **[CHECKLIST.md](../CHECKLIST.md)**.

The condensed top-impact items below are the "if you have only 30 minutes, hit these first" set:

### E-commerce / Payment
```
□ Negative quantity / decimal quantity (skuQty=0.02, FoodNum=0.01) in cart
□ Drop required fields (delete prizeIdList) to coerce free tier
□ amount=999999999 integer overflow → final 0
□ Apply multiple conflicting coupons via array params
□ Race condition: double-spend gift card / same coupon
□ Skip payment step directly to order confirmation  
□ Server-trusted client status fields (payment_status=paid, success:true)
□ Refund without return (trigger refund on delivered item via state change)
□ Multi-device concurrent VIP subscription / 补差价升级
□ Currency rounding exploitation (¥0.019 charge → ¥0.02 wallet credit)
```

### Authentication / Account
```
□ 2FA bypass by direct URL access after password step
□ Filter bypass: ../../path traversal truncation, ;path-parameter truncation
□ Password reset token reuse after email change
□ Weak random reset token: md5(rand()) on Windows PHP, predictable seed
□ Email verification bypass (change email after verification)
□ OAuth account takeover via email match
□ Register with existing unverified email
□ Cookie replacement (admin → user / user → another user)
□ Real-name verification "故意填错" replay-to-reset
```

### Subscriptions / Limits / Resources
```
□ Access premium features after downgrade
□ Exceed rate/usage limits via parallel requests (Turbo Intruder)
□ Referral loop for infinite credits
□ Free trial ≠ time-limited (no enforcement after trial)
□ Direct API call to premium endpoint without subscription check
□ Free-course ID swap to paid-course ID (IDOR on resource)
□ Direct media URL exposure in JSON (.flv / .m3u8 / .mp4 in response)
□ Server-side RBAC residue (sys_menu duplicate rows)
□ Java Web no-Filter / Spring Security antMatchers gap
```

---

## 11. CONSOLIDATED CHECKLIST (2-Hour Full Sweep)

The Section 10 list is the "30-minute money grab". This list is the next layer:
when you have a couple of hours and want a defensive-grade sweep across all
nine business surfaces. It's organized by surface, then by attack mechanism
inside the surface, so you can read a column-down for "what classes of bug
might exist on this endpoint" and a row-across for "where else does this
attack apply".

For full `item / why / verify` triplets including reproduction steps and
tooling per item, load **[CHECKLIST.md](../CHECKLIST.md)**. This section
keeps only the item line for fast scanning.

### 11.1 Login / Authentication
```
□ Username enumeration via response diff (msg / status code / timing)
□ Username enumeration via SMS-send response (sent vs not-registered)
□ Brute force without lockout (no rate limit on failed login)
□ Default / weak credentials (admin/admin, root/123456) on backend & infra
□ 2FA bypass via direct URL after password step / replay 2FA token
□ Client-trusted login flag (status=success, is_login=true in response body)
□ Third-party / SSO callback IDOR (modify uid in callback to take over)
□ Biometric liveness bypass (replay static photo / pre-recorded video)
□ Open redirect in login/register (return_url, redirect, callback param)
□ Hardware-key signature replay / forgery (USB-Key, PKI cert)
```

### 11.2 Registration
```
□ Username / phone / email enumeration via "already exists" response
□ Password strength only enforced client-side (set 123456 server-side)
□ Skip multi-step registration (POST final step directly, miss email verify)
□ Verification code not enforced (empty / random / fixed value passes)
□ SMS / email code replay (same code used twice or across users)
□ Re-register same username after logout, inherit old data / privileges
□ Anti-fraud bypass via N similar virtual accounts (same device, diff email)
□ Mass-register replay-protection missing (no nonce on submit step)
```

### 11.3 Password Recovery / Reset
```
□ Reset target tampering (uid / email / phone in submit step)
□ Reset token predictable (timestamp-derived, weak hash, short random)
□ Cross-user token reuse (A's reset_token, change B's password)
□ Old-password check missing on logged-in change-password endpoint
□ Skip code-verify step, hit final reset endpoint directly
□ Reset link / answer / token leaked in HTML or JS source
□ Reset token has no expiry / not invalidated after use
□ Reset code base64-only "obfuscated" in response
□ Inconsistent identity across multi-step flow (reset_token from step 2
  reusable in step 4)
□ Old session not revoked after email/phone re-bind
```

### 11.4 Session / Token
```
□ Session fixation: pre-login session id remains valid after login
□ Token not bound to user/IP/device (steal cookie → use anywhere)
□ Forged token: weak algorithm md5(username + timestamp), no server salt
□ Stale token still accepted after logout / expiry (no blacklist)
□ Cookie tampering (uid / role / is_admin in cookie trusted server-side)
□ State-machine replay (replay "claim red packet" → re-claim)
□ Anti-replay missing on one-time tokens (CSRF token, OTP, nonce)
□ Sensitive credentials (token, answer, key) hardcoded in front-end JS
□ Privileged session created from public Session ID without re-auth
□ Token works cross-environment (different IP, different UA, no validation)
```

