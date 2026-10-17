# Worked case: the old schema points to the wrong method

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Build a justified next testing route from a bundle and captured responses.

```text
authorized host=app.example.invalid
old docs: GET /api/v1/export
current client: POST /api/v2/export, body={projectId: owned-p1}
GET /api/v1/export -> generic 404
captured POST /api/v2/export under member -> 202, jobId=owned-j1
no captured job-result request
```

**First approach and failure.** Repeating GET on the obsolete route would not establish the current export workflow or its access boundary.

**Revised approach.** Use the captured POST as the reachable entry. Record the job identifier and the missing retrieval step; route the job ownership question to object authorization.

**Independent controls.** Preserve host, method, body keys, principal, and evidence source. The job creation response is a reachability control, not proof that a result is readable.

**Completed result and limits.** Inventory and next boundary are complete for the supplied evidence. Export contents, cross-tenant access, and undocumented hosts remain untested.
