"""Synthetic integer-credit ledger. No provider, money, or concurrency."""

def refund(order, request_key, ledger, request_results, enforce_business_key=False):
    if request_key in request_results:
        return request_results[request_key]
    operation = "full-refund:" + order["id"]
    if enforce_business_key and operation in ledger:
        result = "already-refunded"
    else:
        key = operation if enforce_business_key else request_key
        ledger[key] = order["paid_cents"]
        result = "refunded"
    request_results[request_key] = result
    return result
