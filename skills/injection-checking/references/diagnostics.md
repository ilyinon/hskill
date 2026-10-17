# injection-checking: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Final interpreter and representation | Trace the value past decoding and serialization to its actual consumer. |
| Observed semantic effect | Distinguish literal data, parsed syntax, and the requested impact. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Markup-like text appears in JSON | Data or a later HTML sink | Inspect the consuming code before opening XSS payload catalogs. |
| Arithmetic text changes output | Client computation, template, expression engine, or normal business calculation | Locate the server/client evaluator and compare literal controls. |

## Interpret failure and finish the task

A failed payload for the wrong interpreter does not disprove injection elsewhere. Once the real sink is known, skip unrelated injection families.

Track `controlled value -> transformations -> final interpreter/data sink -> supported semantic effect -> specialist`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Use [XSS context diagnostics](../../xss-cross-site-scripting/references/diagnostics.md) for the final parser question.
