# anti-debugging-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact detection branch | Locate the observed predicate, environment input and resulting exit/failure path. |
| Behavior to preserve | Compare normal and instrumented traces under the same workload before altering a copy. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Debugged run exits early | Debugger detection, missing input, timing/load or environment difference | Locate the first divergent branch and its inputs. |
| One check is bypassed | Analysis path restored or another integrity check now fails | Compare original behavior and later trace rather than declaring all protection gone. |

## Interpret failure and finish the task

A debugger/plugin failure before program execution is setup failure. Timing differences alone do not identify a detector, and patching may change the program being analyzed.

Track `controlled environment -> detector input -> exact branch -> preserved analysis behavior`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
