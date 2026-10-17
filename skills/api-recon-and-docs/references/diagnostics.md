# api-recon-and-docs: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Evidence provenance | Record source bundle/schema version, host, method, and caller context. |
| Reachability and coverage | Separate a route string from a response of the expected handler. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| OpenAPI contains an admin endpoint | Documentation only, stale route, or reachable protected handler | Compare schema provenance with captured requests and handler responses. |
| Path returns an empty list | Valid empty account, denied visibility, or wrong environment | Inspect identity and response schema before recording coverage. |

## Interpret failure and finish the task

A failed schema download is a tooling/access gap, not absence of an API. A stale route remains a lead; discovering another hostname does not add it to active scope.

Track `provenance-linked clue -> in-scope host/method -> reachable handler -> identity/object inventory -> useful handoff`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
