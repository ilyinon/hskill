# windows-av-evasion: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact control and harmless test scope | Record OS/control configuration, test process identity and benign artifact/action. |
| Independent execution and telemetry views | Separate scan verdict, execution result, event collection and alert-generation rules. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| No alert appears | No triggering behavior, collection gap, delayed rule or limited control outcome | Check known-good event collection and the actual local action. |
| One control allows a sample | That control/profile result, not every detection layer | Correlate independent telemetry instead of claiming invisibility. |

## Interpret failure and finish the task

A sensor/test-harness failure cannot prove evasion. Preserve logs and controls; do not add live security-control tampering to a benign evidence review.

Track `benign test action -> actual execution/result -> collection health -> control-specific verdict -> bounded conclusion`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
