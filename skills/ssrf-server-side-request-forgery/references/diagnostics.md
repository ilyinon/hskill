# SSRF: locate the destination-policy failure

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Which component makes the request? | Trace input to the fetch call or correlate its server log; a recursive DNS resolver is not the application identity. |
| What destinations are allowed? | Read the configured scheme/host/address policy and an accepted baseline. Without policy, distinguish fetching from a violation. |
| Who handles redirects and DNS? | Identify client redirect defaults, per-hop validation, and which resolution selects the connection address. |
| What does this primitive expose? | Separate DNS, HTTP request, returned body, method/header control, and reachable destinations. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Callback has DNS but no HTTP | Validator-only resolution, blocked fetch, another resolving component | Correlate local logs/call path; keep HTTP ability unknown until attributed. Do not jump to metadata recipes. |
| Public URL succeeds, restricted URL fails | Correct policy, egress denial, unsupported scheme, or application wrapper | Compare fetch error provenance with the same accepted baseline; inspect the actual validation/connection stage. |
| Direct foreign host is denied; an allowed URL succeeds | Correct first-hop filter; redirect destination may still escape it | Inspect each recorded Location and whether the same policy is applied before each connection. |
| Client command fails before sending | Tool syntax, proxy configuration, encoding, or unsupported transport | Establish one valid baseline with that client; no SSRF hypothesis is disproved by a local setup error. |
| Status/time changes without correlated request | Cache, retries, queueing, content variation | Use source or attributed request evidence; repeating an uncorrelated timing probe does not isolate the cause. |

A valid denial disproves only the tested path/capability. A complete source path with a fetch contract can prove a missing control without a production callback.

## Close the requested task

Track `controlled URL → selected destination → attributable fetch → returned data/action`, marking each edge proved or unknown. For a code audit, identify the missing validation point and the affected flow. For a permitted lab objective, continue only along needed, supported edges. A DNS event alone leaves later edges open. For a fix, apply equivalent policy on redirect hops and verify accepted/denied controls; do not claim this toy host filter handles every production parser/address case.
