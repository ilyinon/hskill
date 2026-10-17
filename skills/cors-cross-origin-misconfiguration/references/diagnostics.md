# cors-cross-origin-misconfiguration: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Complete browser send/read contract | Record origin, credentials mode, cookie eligibility, ACAO/ACAC, and preflight where applicable. |
| Sensitive representation and policy | Identify which identity owns the bytes and why the requesting origin must not read them. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| CLI receives a private response | Server access or browser-readable response | Evaluate cookie dispatch and CORS exposure separately. |
| ACAO is wildcard with credentials | Headers look permissive or browser exposure is blocked | Use the browser credentialed-read rule, not header presence alone. |

## Interpret failure and finish the task

A browser harness failure before dispatch is not a server-policy result. A CORS read denial does not prove CSRF state-change protection.

Track `origin and session -> browser request dispatch -> server response -> browser script exposure -> protected data`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
