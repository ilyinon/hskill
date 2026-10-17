# expression-language-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Evaluator and input position | Distinguish expression source, variable value, property access and normal template text. |
| Evaluation capabilities | Identify exact framework/build, evaluation context and available object/property access. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Arithmetic text appears literally | Variable data, escaped source, or unexecuted branch | Trace the evaluator call and compare a supported expression baseline. |
| Arithmetic evaluates | Expression capability, not necessarily method/type execution | Inspect permitted operations before escalating the claim. |

## Interpret failure and finish the task

A syntax error for a different EL dialect is not a negative for the actual evaluator. Evaluation and unrestricted runtime access are separate capabilities.

Track `input -> expression source/data binding -> evaluator context -> permitted semantic effect -> requested finding/fix`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
