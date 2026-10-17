# linux-security-bypass: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Which control denied? | Separate shell policy, filesystem flags, LSM, namespace and syscall restrictions. |
| Actual operation and error provenance | Compare the requested action with a permitted baseline under the same identity. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Writing a file fails | Read-only mount, DAC/ACL or MAC policy | Correlate mount flags and enforcement log/errno. |
| One alternative executes | A narrower restriction was bypassed or a permitted path was used | State which policy edge changed; do not infer every control disappeared. |

## Interpret failure and finish the task

A helper syntax error did not exercise the control. Do not delete logs or disable auditing to validate a boundary; preserve supplied denial evidence.

Track `principal/context -> requested operation -> identified enforcement gate -> permitted alternative or bounded denial`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
