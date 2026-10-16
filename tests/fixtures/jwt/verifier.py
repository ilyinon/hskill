"""Minimal HS256 policy fixture, not a production JWT implementation."""
import base64, hashlib, hmac, json
KEY = b"offline-fixture-key-not-a-production-secret"

def decode(part):
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))

def verify(token):
    try:
        header, payload, signature = token.split(".")
        if decode(header).get("alg") != "HS256":
            return None
        expected = base64.urlsafe_b64encode(hmac.new(KEY, (header + "." + payload).encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
        if not hmac.compare_digest(signature, expected):
            return None
        claims = decode(payload)
        if claims.get("iss") != "fixture-issuer" or claims.get("aud") != "fixture-api":
            return None
        return claims
    except (ValueError, TypeError, UnicodeError):
        return None
