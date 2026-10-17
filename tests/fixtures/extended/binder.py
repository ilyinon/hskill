def bound_item(pairs):
    values = [value for name, value in pairs if name == "item"]
    if len(values) != 1:
        raise ValueError("one item required")
    return values[0]
def read(pairs, allowed, records):
    item = bound_item(pairs)
    if item not in allowed:
        return 403, None
    return 200, records[item]
