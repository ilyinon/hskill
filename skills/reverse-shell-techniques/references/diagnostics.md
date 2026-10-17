# reverse-shell-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Requested proof and authorized connection | Establish whether a session is actually needed and which endpoints/actions are permitted. |
| Platform and transport prerequisites | Record execution context, listener direction, egress, DNS, protocol and terminal requirements. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Listener starts successfully | Local readiness, not target reachability | Trace the owned client path and handshake. |
| A connection arrives | Expected identity/session or unrelated traffic | Correlate an inert nonce and supplied destination identity before claiming control. |

## Interpret failure and finish the task

A wrong address, blocked egress or protocol mismatch is a connection/setup failure, not proof that command execution is absent. Stop when a smaller requested marker already completes the task.

Track `permitted local execution -> compatible connection path -> authenticated owned endpoint -> requested bounded session/effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
