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

## Verify per-message authorization

Review authentication and origin policy at the handshake and enforce authorization again on each privileged message. Check how the connection handles an expired or revoked session and apply size and rate limits. In dispatcher tests, confirm that an approved action reaches its handler and a denied action leaves state untouched. Preserve event metadata without logging session tokens or raw private message contents. [OWASP WebSocket Security](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)
