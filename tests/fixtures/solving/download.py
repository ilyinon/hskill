"""Synthetic parent/child authorization model; no files or users are accessed."""

def attachment(session, parent_id, attachment_id, parents, children, bind_child=False):
    parent = parents[parent_id]
    if (parent["owner"], parent["tenant"]) != (session["user"], session["tenant"]):
        return 403, None
    child = children[attachment_id]
    if bind_child and child["parent"] != parent_id:
        return 403, None
    return 200, child["body"]
