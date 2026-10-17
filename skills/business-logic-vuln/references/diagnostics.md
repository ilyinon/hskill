# business-logic-vuln: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Domain invariant and units | Specify allowed transitions and durable value/state, not just response counts. |
| Ordering evidence | Separate sequential repetition from a demonstrated concurrent interleaving. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Repeated success responses | Cached retry, legitimate partial operation, or excess effect | Count committed per-object effects. |
| Only concurrent calls break the rule | Possible check/use race | Locate the shared state and exact interleaving before routing to race analysis. |

## Interpret failure and finish the task

If sequential repetition already violates the rule, fix the domain invariant before blaming timing. Parser errors belong to the actual interpreter path, not automatically business logic.

Track `domain contract -> operation identity/state -> observed durable violation -> business or concurrency specialist`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Use [business-logic diagnostics](../../business-logic-vulnerabilities/references/diagnostics.md); use [race-condition](../../race-condition/SKILL.md) when an interleaving matters.
