"""Synthetic partial-credit model, sequential and offline."""
def credit(order, amount, request_id, ledger, seen):
    if request_id in seen:
        return seen[request_id]
    if amount <= 0 or amount > order["paid_cents"]:
        return "denied"
    ledger.append({"order": order["id"], "amount": amount})
    seen[request_id] = "credited"
    return "credited"
