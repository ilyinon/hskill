"""Synthetic in-memory authorization exercise; no server or database."""
INVOICES = {"a1": {"owner": "alice", "tenant": "A", "total": 17},
            "b1": {"owner": "bob", "tenant": "B", "total": 29}}

def read_invoice(session, invoice_id):
    if not session:
        return 401, {"error": "login required"}
    return 200, INVOICES[invoice_id]

def read_invoice_checked(session, invoice_id):
    if not session:
        return 401, {"error": "login required"}
    record = INVOICES[invoice_id]
    if record["owner"] != session["user"] or record["tenant"] != session["tenant"]:
        return 403, {"error": "forbidden"}
    return 200, record
