# sandbox-escape-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact sandbox boundary | Identify language evaluator, process/filesystem namespace, syscall policy and stated forbidden capability. |
| Starting capabilities and context | Record available objects/operations and the denied baseline under the same identity. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Code evaluates inside sandbox | Intended computation or authority outside policy | Inspect the requested resource/syscall effect. |
| A language restriction is bypassed | One layer changed; OS/process controls may still apply | Trace the next enforcement layer independently. |

## Interpret failure and finish the task

A syntax/import failure is not proof of OS containment. Conversely, executing permitted arithmetic does not establish escape from an access-control boundary.

Track `initial sandbox capability -> language/process operation -> next policy gate -> prohibited resource/effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
