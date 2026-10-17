# http-parameter-pollution: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Every parser and binding rule | Record first/last/list/reject behavior for the exact content type at each layer. |
| Security decision and consumer | Identify which selected value is validated and which drives the protected action. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Duplicate keys accepted | Consistent parser semantics or validator/consumer disagreement | Use distinct inert markers and trace both selected values. |
| Proxy rejects duplicates | Parser failure before application or effective shared policy | Correlate whether the application handler runs. |

## Interpret failure and finish the task

A duplicate-key error is not a bypass. Product names do not establish first/last behavior; the concrete parser chain must be observed.

Track `raw duplicate fields -> validator selection -> application binding -> protected object/action`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
