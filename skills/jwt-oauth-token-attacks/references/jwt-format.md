# JWT format and untrusted claims

Read when identifying token structure or decoding a supplied compact JWS. Never send a supplied token to an external decoder.

## 1. JWT ANATOMY

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMzQsInJvbGUiOiJ1c2VyIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
└─────────────────────┘ └────────────────────────────┘ └──────────────────────────────────────────┘
         HEADER                     PAYLOAD                           SIGNATURE
```

**Decode without verifying** (JWS uses Base64url, with optional omitted padding):
```python
import base64, json
part = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
header = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
print(header)
```

Decoding reveals untrusted data; acceptance requires the verifier's signature and claim policy. This three-part example is a compact JWS; encrypted JWTs use a different structure. [RFC 7515](https://www.rfc-editor.org/rfc/rfc7515.html).

**Claim-policy candidates** (a change matters only if accepted with forbidden authority):
```json
{
  "role": "admin",
  "isAdmin": true,
  "userId": "OTHER_TEST_USER_ID",
  "email": "other-test-user@example.invalid",
  "sub": "admin",
  "permissions": ["admin", "write", "delete"],
  "tier": "premium"
}
```
