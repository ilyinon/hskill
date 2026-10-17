# windows-privilege-escalation: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Effective token and security boundary | Distinguish standard user, filtered administrator, integrity and enabled privileges. |
| Privileged consumer of controlled path | Resolve service/task executable, argument parsing, ACLs and actual writable resource. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A directory is writable | Unconsumed path, correct executable or intercepted lookup candidate | Resolve the actual service binary and full path ACL. |
| An elevated administrator action succeeds | Expected administrator elevation or a standard-user crossing | Keep starting account/token explicit. |

## Interpret failure and finish the task

A named privilege or old compatibility row is a candidate. A service restart/setup failure cannot prove code ran as its account.

Track `starting token -> controlled file/configuration -> actual privileged consumer -> observed identity/capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
