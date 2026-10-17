# active-directory-acl-abuse: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Effective subject/object permission | Resolve group membership, ACE scope, inheritance, object type and ownership for this target. |
| Reachable downstream use | Identify which concrete directory attribute/action the effective right permits. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Graph shows a powerful edge | Stale collection, inherited-object mismatch or effective permission | Compare current object ACL/type and actual token groups. |
| Named right appears | It may apply only to a different property/object class | Evaluate scope before selecting a write or escalation chain. |

## Interpret failure and finish the task

A directory tool failure is not a permission denial. A permission on one object does not establish a path to a different object; writes require the already agreed scope and rollback.

Track `current principal/groups -> effective scoped ACE -> target operation -> resulting capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
