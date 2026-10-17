# macos-security-bypass: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact protection and responsible identity | Record TCC/Gatekeeper/SIP/sandbox/signing context and OS build separately. |
| Actual protected operation | Correlate permission/prompt state with the process that opens the resource. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A privacy database row says allow | Different identity, stale row or effective grant | Compare responsible process identity and actual resource result. |
| Quarantine/signing state changes | One prerequisite changed, not every policy | Trace the final launch/access decision for the stated threat model. |

## Interpret failure and finish the task

A permission-tool error is a setup gap. Admin/debug access or a historical CVE does not establish a bypass under a standard release identity.

Track `process identity -> applicable policy/grant -> protected operation -> observed allowed or denied effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
