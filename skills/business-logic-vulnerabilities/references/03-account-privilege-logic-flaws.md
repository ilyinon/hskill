# business-logic-vulnerabilities technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. ACCOUNT / PRIVILEGE LOGIC FLAWS

### Email Verification Bypass
```
1. Register with email A (legitimate, verified)
2. Change email to B (attacker's email, unverified)
3. Use account as verified — does server enforce re-verification?

Or: Change email to victim's email → no verification → account claim
```

### Password Reset Token Binding
```
1. Request password reset for your account → get token
2. Change your email address (account settings)
3. Reuse old password reset token → does it still work for old email?

Or: Request reset for victim@target.com
    Token sent to victim but check: does URL reveal predictable token pattern?
```

### OAuth Account Linking Abuse
```
1. Have victim's email (but not their password)
2. Register with victim's email → get account with same email
3. Link OAuth (Google/GitHub) to your account
4. Victim logs in with Google → server finds email match → merges with YOUR account
```

### Session Identity Control — Horizontal/Vertical Authorization

A valid administrator session represents the administrator; replacing a user's session with it does not prove escalation.

For an authorization check, preserve Account A's low-privilege session while changing only the requested resource to Account B's authorized test object, or requesting a function A is not permitted to use. Compare with an authorized baseline and record the subject, object, and expected policy. Do not log out or revoke a supplied session.

A login redirect without cookies and a data response with a user cookie establishes authentication behavior. It proves an authorization flaw only when that same user can access data or actions forbidden by the intended policy.

### Permission Residue from Database Inconsistency

A subtle case from the second audit class: the admin UI shows that role X has had permission `user:list` revoked, but querying the SQL data:

```sql
SELECT * FROM sys_menu WHERE role_id = 2;
-- two rows for the same menu_id "user:list"
```

The UI's "remove permission" only deleted ONE row; the duplicate row keeps the API accessible. Verify by:
```sql
SELECT menu_id, COUNT(*) FROM sys_menu GROUP BY menu_id, role_id HAVING COUNT(*) > 1;
```

Lesson: when a UI says permission revoked but API still works → check the underlying RBAC table for duplicates / orphaned grants.

### Weak-Random Password Reset Token

PHP / legacy stack on Windows uses `rand()` whose `RAND_MAX = 32768`. If a reset link uses
`/resetpassword.php?id=md5(rand())`, the entire keyspace is precomputable:
```php
$a = 0;
for ($a = 0; $a <= 32768; $a++) {
    $b = md5($a);
    echo $b . "\r\n";
}
```
Iterate the resulting dictionary against `/resetpassword.php?id=<hash>` — when one returns a valid reset page you can change the victim's password. Audit any token generation that ultimately calls `rand()`, `mt_rand()` (without seeding), `Random()` (default seed in C#), etc.

---

## 6. API BUSINESS LOGIC FLAWS

### Object State Manipulation
```
order.status = "pending"
→ PUT /api/orders/1234 {"status": "refunded"}   ← self-trigger refund
→ PUT /api/orders/1234 {"status": "shipped"}    ← mark as shipped without shipping
```

### Transaction Reuse
```
1. Initiate payment → get transaction_id
2. Complete purchase
3. Reuse same transaction_id for second purchase:
   POST /api/checkout {"transaction_id": "USED_TX", "cart": "new_cart"}
```

### Limit Count Manipulation
```
Daily transfer limit = $1000
→ Transfer $999, cancel, transfer $999 (limit not updated on cancel)
→ Parallel transfers (race condition on limit check)
→ Different payment types not sharing limit counter
```

### Java Web "No Filter, No Spring Security" Anti-Pattern

Audit-friendly tell: a Spring Boot project that does **NOT** include `spring-boot-starter-security` and has zero `Filter` classes. This means every controller is wide-open for `guest` unless the developer manually checked the session in each method. Reproduce:
```bash
# Inside the source tree
find . -name "*.java" -exec grep -l "Filter" {} \;     # likely empty
find . -name "*.java" -exec grep -l "@PreAuthorize\|@Secured" {} \;
```
If both are empty, expect almost every API to be unauthorized. From the audit demo:
```java
public Result score(@RequestParam("userId") Integer userId) {
    Score score = scoreService.selectScoreByUserId(userId);
    return Result.success(score);
}
```
No check that `userId` matches the session's logged-in user → horizontal IDOR. Worse: the same endpoint works **without any Cookie**, since nothing forces authentication globally.

### Spring Security `antMatchers` Coverage Gap

The audit videos also showed a partially-secured Spring Security config like:
```java
.antMatchers("/system/user/info").authenticated()
.antMatchers("/system/menu/**").hasRole("admin")
```
A common error is an over-narrow rule — e.g. `/system/user/info` is protected but `/system/user/list` is not, or `/system/menu/**` is admin-only but `/system/dept/treeData` is open. Cross-check the controller annotations (`@PreAuthorize("@ss.hasPermi('system:user:list')")`) against the SecurityConfig — every annotated endpoint must also map to a SecurityConfig rule. Mismatches are common after refactors.

---

## 7. SUBSCRIPTION / TIER CONFUSION

```
Free tier: cannot access feature X
Paid tier: can access feature X

Attack: 
- Sign up for paid trial → enable feature X → downgrade to free
  → Does feature X get disabled on downgrade? 
  → Can you continue using feature X?

Or:
- Inspect premium endpoint list from JS bundle
- Directly call premium endpoints with free account token
→ Server checks subscription for UI but not API?
```

### Direct Media URL Leak — VIP Resource Bypass

Real cases from a fitness/learning app: when the client requests course detail, the JSON response embeds the raw media URL:
```http
GET /gerudo/v2/liveCourse/625020ce8f002700010554c1/detail HTTP/1.1
{
  "previewPullUrl": "http://app-live.../live/app-live_625020ce8f002700010554c2_Preview.flv"
  ...
}
```
Search **all** detail / preview / playback responses for keywords:
```
.flv  .m3u8  .mp4  .mp3  videoUrl  downloadUrl  streamUrl  previewPullUrl
```
For each hit, replay the URL anonymously (curl, VLC, flv.js demo at `https://bilibili.github.io/flv.js/demo/`). If the URL plays without a session, you've broken VIP gating. Defense: use signed, short-TTL URLs bound to user/IP/Referer, not raw resource paths.

### Resource ID Replacement — Free → Paid Course

Companion bug: free course detail returns `{"id": "60caa21e853f5c1651b27c1b", ...}`. Replace the ID in the URL with a known paid course ID. If the response structure remains the same and includes the playable URL → IDOR on premium content. Defense: verify the **owner relation** on each detail call, not just "is logged-in".

---

