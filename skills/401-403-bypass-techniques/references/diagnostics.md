# 401-403-bypass-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Protected representation and principal | Capture an allowed owner response and the unchanged denied session. |
| Request handling layers | Identify proxy rewrites, method handling, and the final application route. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Variant returns 200 | Login shell, cached public page, or protected content | Compare body schema and owned marker, not status alone. |
| HEAD works but GET is denied | Method-specific metadata versus content access | Inspect the permitted response and whether the protected action ran. |

## Interpret failure and finish the task

A malformed path or unsupported method did not test the original authorization decision. A valid generic-page response disproves that variant as a content-access proof, not every possible route.

Track `fixed principal -> normalized route -> authorization -> protected representation/action`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
