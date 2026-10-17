# csrf-cross-site-request-forgery: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Meaningful action and authentication | Record final state, cookie/token binding and required request method/content type. |
| Realistic browser dispatch | Inspect SameSite, Origin, preflight, redirects and whether the action request is sent. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| No anti-CSRF field appears | Alternative binding or missing protection | Trace the exact server predicate and a browser-sendable request. |
| A browser read is blocked | CORS exposure denial or prevented dispatch | Determine whether the state-changing request actually ran. |

## Interpret failure and finish the task

A CLI request with manually inserted victim credentials does not establish browser feasibility. An OPTIONS failure and an executed POST with an unreadable response prove different things.

Track `attacker context -> browser-eligible request/cookies -> server binding check -> committed protected state`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
