"""Offline fixture: fetch is injected; no networking occurs on import."""
def preview(url, fetch):
    return {"preview": fetch(url)}
