# prototype-pollution: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual write operation | Distinguish parsing an own key from invoking a setter or recursively mutating a prototype. |
| Affected object and isolation | Identify target-local prototype changes versus a shared prototype, and reset test state. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| JSON contains __proto__ text | Own data property or a later dangerous write | Inspect actual property descriptors and target lookup. |
| Inherited marker appears | Changed target prototype or shared global prototype | Compare an unrelated fresh object and the target's own keys. |

## Interpret failure and finish the task

A JSON parse by itself does not establish pollution. A library error before the write did not test the primitive; persistent prototype state can contaminate controls.

Track `untrusted key -> actual property write -> affected prototype/lookup -> reachable consumer -> bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

For a confirmed source plus consumer, use [advanced diagnostics](../../prototype-pollution-advanced/references/diagnostics.md).
