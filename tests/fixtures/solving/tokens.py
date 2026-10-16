"""Minimal signed-token model, deliberately incomplete; not a JWT library."""
import base64, hashlib, hmac, json
KEY = b"offline-training-key-never-use-in-production"

def part(value):
    return base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).rstrip(b"=").decode()

def issue(audience):
    header = part({"alg": "HS256", "typ": "JWT"})
    payload = part({"sub": "alice", "iss": "fixture-issuer", "aud": audience})
    signature = base64.urlsafe_b64encode(hmac.new(KEY, (header + "." + payload).encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
    return header + "." + payload + "." + signature

def decode(value):
    return json.loads(base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)))

def report(token, enforce_audience=False):
    try:
        header, payload, signature = token.split(".")
        if decode(header).get("alg") != "HS256":
            return 401, None
        expected = base64.urlsafe_b64encode(hmac.new(KEY, (header + "." + payload).encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
        if not hmac.compare_digest(signature, expected):
            return 401, None
        claims = decode(payload)
        if claims.get("iss") != "fixture-issuer":
            return 401, None
        audiences = claims.get("aud", [])
        if isinstance(audiences, str):
            audiences = [audiences]
        if enforce_audience and "reports" not in audiences:
            return 401, None
        return 200, {"principal": claims["sub"], "body": "report fixture"}
    except (ValueError, TypeError, KeyError, UnicodeError):
        return 401, None
