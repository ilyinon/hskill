# symbolic-execution-tools: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Faithful input and state | Record byte widths, signedness, endianness, initialization and actual input transport. |
| Original acceptance predicate | Distinguish solver constraints/hooks from what the supplied program really checks. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Solver returns SAT | A model candidate, not original acceptance | Replay or independently evaluate the original predicate and input bounds. |
| Path search stalls | State explosion, wrong initialization or unreachable target | Locate the first unmodeled dependency before changing the goal. |

## Interpret failure and finish the task

A solver/tool exception did not disprove satisfiability. Overpermissive hooks and unconstrained input can create answers the original program cannot accept.

Track `original input contract -> faithful model -> candidate -> original predicate/trace -> requested recovered value`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
