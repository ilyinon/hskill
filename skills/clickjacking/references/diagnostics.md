# clickjacking: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Effective ancestor policy | Inspect enforced frame-ancestors/XFO, all ancestors and actual document response. |
| Meaningful browser action | Establish framing, eligible session, interaction, reauthentication and resulting owned state. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Page loads in a frame | Public/anonymous view or a usable authenticated action | Inspect session and action gate. |
| No XFO header | CSP may still restrict framing | Evaluate effective enforced ancestor policy before constructing more UI variants. |

## Interpret failure and finish the task

A blocked frame is a control for that ancestor chain. A visible frame without a completed meaningful action is not the claimed action impact.

Track `framing permission -> victim test session -> interaction -> action-specific check -> protected state change`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
