# api-authorization-and-bola: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Action and field policy | Separate object access, function permission, and which fields are writable by each role. |
| Actual binding layer | Trace deserialization, allowlisted update fields, and the final stored object. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Hidden role field appears in documentation | Administrative schema or a writable field for this principal | Inspect per-action binding and compare final state. |
| Own object update succeeds | Normal edit or mass assignment | Compare permitted label changes with forbidden owner/role changes using the same session. |

## Interpret failure and finish the task

An unknown-field error is not privilege escalation. A rejected role change says nothing about independently loaded child objects; follow their actual parent/owner enforcement.

Track `fixed subject -> action/object policy -> writable-field policy -> committed state`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

For nested object checks, use the canonical [IDOR diagnostics](../../idor-broken-object-authorization/references/diagnostics.md) and [parent/child case](../../idor-broken-object-authorization/references/worked-cases.md).
