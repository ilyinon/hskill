def xml_external_resource(name):
    return {"status": "denied", "opens": 0}
def transform_document(name, supplied_resources):
    # Inert resource-map model of a later resolver; no network or XML engine.
    return supplied_resources[name]
