# linux-privilege-escalation: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Effective identity and actual policy | Record UID/groups, sudo/capabilities, mount semantics and enforcement context. |
| Privileged use of a controlled resource | Trace writable data into a root-context executable, task, service or parser. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A script is writable | Unused file, unprivileged consumer or privileged task | Resolve the actual scheduler/service path and effective user. |
| SUID/capability label appears | A prerequisite, not the resulting authority | Inspect runtime restrictions and an observed permission effect. |

## Interpret failure and finish the task

A version-string match or enumeration error is not a working local path. Fix the earliest missing consumer/permission fact before choosing an exploit recipe.

Track `low-privilege principal -> controlled resource -> actual privileged consumer -> bounded permission effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
