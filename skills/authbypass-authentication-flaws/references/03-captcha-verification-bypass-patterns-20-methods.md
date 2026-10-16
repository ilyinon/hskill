# authbypass-authentication-flaws technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 11. CAPTCHA/VERIFICATION BYPASS PATTERNS (20 Methods)

| # | Method | How |
|---|---|---|
| 1 | Remove captcha parameter | Delete captcha field from request |
| 2 | Send empty captcha | `captcha=` or `captcha=null` |
| 3 | Reuse previous captcha | Same captcha value works multiple times |
| 4 | Captcha not bound to session | Use captcha solved in session A for session B |
| 5 | Server-side validation missing | Captcha checked client-side only |
| 6 | Response manipulation | Intercept and change response to bypass |
| 7 | Change request method | POST→GET or vice versa may skip captcha check |
| 8 | JSON content-type | Switch from form to JSON — captcha handler may not process |
| 9 | OCR bypass | Simple captchas solvable with tesseract/ML |
| 10 | Audio captcha weakness | Audio often simpler than visual |
| 11 | SMS code in response | Verification code returned in API response body |
| 12 | SMS code predictable | Sequential or time-based codes |
| 13 | No rate limit on code verification | Brute-force 4-6 digit code |
| 14 | Code not bound to phone/email | Use code sent to phone A on account B |
| 15 | Code doesn't expire | Old codes remain valid |
| 16 | Null byte in phone number | `+1234567890%00` bypasses dedup but delivers to same number |
| 17 | Case sensitivity | Email: `Admin@X.com` vs `admin@x.com` |
| 18 | Space/encoding in identifier | `user@x.com` vs `user@x.com ` (trailing space) |
| 19 | Concurrent requests | Race condition: send verify before captcha loads |
| 20 | Third-party captcha bypass | Misconfigured reCAPTCHA site key allows any domain |

---

## 12. INSECURE RANDOMNESS — TOKEN PREDICTION

### UUID v1 (Time-Based — Predictable!)

```
UUID v1 format: timestamp-clock_seq-node(MAC)
# MAC address often leaked via other endpoints
# Timestamp is 100ns intervals since 1582-10-15
# Tool: guidtool (reconstruct possible UUIDs from known timestamp range)
```

### MongoDB ObjectId

```
ObjectId = 4-byte timestamp + 5-byte random + 3-byte counter
# First 4 bytes = Unix timestamp → creation time leaked
# Counter is sequential → adjacent ObjectIds predictable
# If you know one ObjectId, nearby ones are calculable
```

### PHP uniqid()

```php
uniqid() = hex(microtime)
// Output: 5f3e7a4c1d2b3
// Entirely based on current microsecond timestamp
// Predictable if you know approximate server time
```

### PHP mt_rand() Recovery

```
# mt_rand() uses Mersenne Twister PRNG
# After observing ~624 outputs, full internal state is recoverable
# Tool: openwall/php_mt_seed
# Feed known outputs → recover seed → predict all future values
```

### Tools

- `guidtool` — UUID v1 reconstruction
- `AethliosIK/reset-tolkien` — Automated token prediction for password resets
- `openwall/php_mt_seed` — PHP mt_rand seed recovery
- `sandwich` — Token timestamp analysis
