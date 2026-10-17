# attack-surface-mapping: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Product and permitted assets | Start from the supplied application and authorization, including roles and tenants. |
| Provenance of each edge | Link routes, transforms, IDs, and dependencies to captured traffic or source. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Only a login page is visible | Unauthenticated view or genuinely small surface | Inspect supplied client/traffic for actual workflows before enumeration. |
| Client mentions another host | Business dependency or newly authorized target | Record the relationship and scope gap without probing it. |

## Interpret failure and finish the task

A crawler failure or unauthenticated shell is a coverage limit. An empty tenant-specific list does not mean the object type is absent.

Track `authorized app -> observed role/workflow -> endpoint and object edges -> unresolved boundary -> specialist handoff`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
