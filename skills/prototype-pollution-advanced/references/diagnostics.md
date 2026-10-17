# prototype-pollution-advanced: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Confirmed source and exact lookup | Start from an observed mutation, then identify own/inherited reads at a reachable consumer. |
| Gadget preconditions and state | Pin runtime/library, defaulting behavior, call site and clean-process controls. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Prototype marker is visible | Primitive only or a consumed option | Trace the actual option read and resulting operation. |
| Own option shadows the marker | Consumer ignores inheritance on this path | Compare inherited-only and explicit own-value cases. |

## Interpret failure and finish the task

A historical gadget name does not prove reachability. Clean controls must not share persistent polluted state; a guarded consumer can break a valid pollution-to-effect chain.

Track `confirmed source -> inherited property -> consumer guard/default -> protected behavior`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
