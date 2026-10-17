# unauthorized-access-common-services: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Service identity and policy | Pin actual protocol, version, current principal/ACL and intended public/private operations. |
| Specific protected command | Distinguish handshake/liveness from sensitive read, write, administration or execution. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| PONG/banner is returned | Public liveness or unrestricted command authority | Inspect command ACL and a permitted protected-operation observation. |
| Management UI loads | Static/login shell or authenticated management | Compare principal and actual action result. |

## Interpret failure and finish the task

A client protocol mismatch is not a valid negative. An allowed liveness command does not establish that persistence, files, modules or administrative commands are permitted.

Track `network reachability -> protocol identity -> effective authentication/ACL -> specific protected capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
