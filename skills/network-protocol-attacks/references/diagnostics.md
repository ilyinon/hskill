# network-protocol-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual segment/client/protocol | Record vantage, permitted peers, active protections and the relevant discovery/routing flow. |
| Receiving-peer decision | Separate emitted spoofed traffic from accepted cache/route/identity changes. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Broadcast query is visible | Network position, not automatic impersonation | Inspect whether the peer accepts a competing answer. |
| Spoofed packet is sent | Only transmission or an effective mapping/routing change | Correlate receiver state and subsequent owned test traffic. |

## Interpret failure and finish the task

A packet-generator error did not exercise the network. A broadcast or response capture alone is not interception; avoid expanding tests across unrelated segments.

Track `network position -> controlled protocol message -> receiving peer acceptance -> changed mapping/route -> bounded traffic effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
