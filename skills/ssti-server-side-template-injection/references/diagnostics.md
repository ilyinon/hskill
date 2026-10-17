# ssti-server-side-template-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Input as source or data | Trace template compilation separately from rendering variables and client interpolation. |
| Exact engine/context | Identify runtime, sandbox, available objects and integration before engine-specific techniques. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| {{7*7}} is displayed literally | Data binding, escaping, or an unexecuted compile branch | Inspect the render call and a source-template baseline. |
| 49 appears | Server template evaluation, client code, or normal arithmetic | Correlate the actual evaluator; arithmetic alone does not identify engine or RCE. |

## Interpret failure and finish the task

A parser error for an unrelated dialect is not class-wide disproof. A variable value is not recursively compiled unless the actual path performs that step.

Track `input -> source/data position -> compilation/rendering -> observed evaluation -> separately supported capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
