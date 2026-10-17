# file-access-vuln: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual stage and sink | Separate path read/include, archive extraction, upload processing, and final serving. |
| Ownership versus filesystem root | Determine whether the wrong object or an out-of-root path caused the result. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Uploaded bytes are retrieved privately | Expected storage or a handler/content boundary | Inspect processor and serving behavior. |
| Download returns another tenant file | Object authorization or traversal | Check identifier lookup and resolved path separately. |

## Interpret failure and finish the task

A successful upload is not execution. An opaque ID selecting a foreign object should route to authorization rather than inventing traversal syntax.

Track `input -> accept/store/process/serve or path lookup -> violated policy -> matching specialist`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Use [IDOR](../../idor-broken-object-authorization/SKILL.md), [path diagnostics](../../path-traversal-lfi/references/diagnostics.md), or [upload diagnostics](../../upload-insecure-files/references/diagnostics.md) for the observed stage.
