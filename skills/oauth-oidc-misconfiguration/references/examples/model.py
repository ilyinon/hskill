"""Identity lookup after an assumed, separately validated OIDC callback."""

def account(claims, accounts, include_issuer=False):
    if include_issuer:
        return accounts.get((claims["iss"], claims["sub"]))
    for (issuer, subject), local_user in accounts.items():
        if subject == claims["sub"]:
            return local_user
    return None
