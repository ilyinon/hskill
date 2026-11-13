# upload-insecure-files: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| All pipeline stages | Trace accept/store/process/serve, final identifiers and the ownership policy. |
| Actual handler/context | Determine whether bytes execute, render as active content, stay data or trigger a processor. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Dangerous extension uploads successfully | Stored inert data or an executable/active handler | Inspect final serving handler and observed effect. |
| Upload is private but preview is public | Separate access-control decision at a later stage | Compare same-ID retrieval across owned accounts and sharing policy. |

## Interpret failure and finish the task

A processor failure did not prove execution. An upload result is an intermediate capability, not automatically RCE, private read or overwrite.

Track `owned input -> acceptance -> storage -> processing -> serving identity/context -> requested effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Verify storage and delivery controls

Give stored objects application-generated names. Keep uploads outside executable web roots and validate type and size before processing. Authorize every download against the stored object's owner or tenant. Check that a supported document round-trips, a rejected input creates no stored object, and a download by a different tenant is denied. Review response media type and disposition for untrusted content. [OWASP File Upload Guidance](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
