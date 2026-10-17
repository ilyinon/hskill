def invoice(session, item_id, records):
    if session is None:
        return 401, None
    return 200, records[item_id]
