# dependency-confusion: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual ecosystem and resolution policy | Read package source routing, lockfile, constraints, and install mode. |
| Execution versus selection | Separate package source choice, download, integrity, and lifecycle-script permission. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Public candidate has a higher version | Eligible resolution or irrelevant registry | Inspect the configured source and lock selection. |
| Install log mentions public registry | One unrelated dependency or protected name resolved there | Attribute the exact package/version/integrity/source. |

## Interpret failure and finish the task

An install failure before resolution is not proof of source protection. An eligible public candidate is not proof it was selected, and selection is not lifecycle-code execution.

Track `protected dependency -> routing/constraints/lock -> selected source and integrity -> permitted install behavior`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
