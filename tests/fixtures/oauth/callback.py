"""Offline PKCE/session-binding model; no identity-provider requests."""
import base64, hashlib, hmac

def callback(session, code, pending, issued):
    transaction = pending.get(session)
    grant = issued.get(code)
    if not transaction or not grant or grant["used"]:
        return None
    challenge = base64.urlsafe_b64encode(hashlib.sha256(transaction["verifier"].encode()).digest()).rstrip(b"=").decode()
    if grant["client"] != transaction["client"] or grant["redirect_uri"] != transaction["redirect_uri"]:
        return None
    if not hmac.compare_digest(challenge, grant["challenge"]):
        return None
    grant["used"] = True
    return grant["subject"]
