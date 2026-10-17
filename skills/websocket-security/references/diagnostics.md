# websocket-security: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Handshake and browser conditions | Record Origin/session/cookie eligibility and the accepted channel identity. |
| Per-message policy | Trace subscription/object/action authorization after the 101 handshake. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Handshake returns 101 | Transport works or unauthorized data is reachable | Inspect subscription acknowledgements and actual protected frames. |
| Origin is accepted | Intended origin policy or CSWSH candidate | Establish browser credential dispatch and meaningful channel capability. |

## Interpret failure and finish the task

A failed WebSocket client setup did not test server authorization. An authenticated connection is not permission for every topic or message action.

Track `browser/session -> handshake identity -> message/topic authorization -> protected frame/state`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
