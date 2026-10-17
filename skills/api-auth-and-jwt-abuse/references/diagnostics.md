# api-auth-and-jwt-abuse: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Credential extraction and caller | Trace bearer/API-key parsing and the resulting principal/scopes. |
| Proxy trust | Record the immediate peer and which forwarded headers are stripped or replaced. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Identity header changes but result does not | Ignored header, trusted-hop enforcement, or endpoint-level denial | Inspect the consumed value and resulting principal. |
| Valid credential plus forged role header returns data | Credential legitimately allowed it or header influenced authorization | Compare the same credential without the header and a forbidden capability. |

## Interpret failure and finish the task

A token-parser error needs a known-good credential baseline. A correctly ignored untrusted proxy header is a controlled negative for that header path; token trust and object permissions remain separate.

Track `wire credential/header -> trusted extraction -> principal/scopes -> protected operation`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
