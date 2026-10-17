# graphql-and-hidden-parameters: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Resolver path and fixed principal | Trace each returned field, nested resolver, and object/tenant permission. |
| Discovery versus capability | Separate introspection/batching support from protected read/write or budget violation. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Introspection is disabled | One discovery channel blocked or fields truly absent | Use supplied source/schema/client calls; do not equate introspection denial with authorization. |
| Parent object is authorized | Nested child inherits policy or independently loads a foreign object | Inspect child resolver and compare ownership in the same session. |

## Interpret failure and finish the task

A query validation error does not test resolver authorization. A field in a schema does not prove it is writable, readable, or sensitive for the current principal.

Track `fixed principal -> query field -> parent resolver -> selected nested object -> returned protected data`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
