"""Synthetic redirect model. All responses are supplied; no network exists."""
from urllib.parse import urlsplit, urljoin

def preview(url, responses, allowed_host, validate_each_hop=False):
    trace = []
    for hop in range(4):
        if hop == 0 or validate_each_hop:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or parsed.hostname != allowed_host:
                return {"status": "denied", "trace": trace}
        trace.append(url)
        response = responses[url]
        if "location" in response:
            url = urljoin(url, response["location"])
        else:
            return {"status": "ok", "body": response["body"], "trace": trace}
    return {"status": "hop-limit", "trace": trace}
