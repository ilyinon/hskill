# insecure-source-code-management: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Returned artifact bytes | Compare content signature/structure with a nonexistent-path control. |
| Acquisition goal and trust | Bound recovery to needed evidence; treat recovered hooks/config as untrusted data. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Directory returns 403 | Generic deny rule or real repository path | Inspect a permitted direct metadata response and control. |
| HEAD-looking text exists | Authentic metadata, test text, or catch-all response | Compare content types, unrelated paths, and repository object structure before reconstruction. |

## Interpret failure and finish the task

A dumper failure does not prove absence of exposure; a catch-all page is not repository metadata. Secret exposure and live credential validity require separate conclusions.

Track `path candidate -> authentic artifact bytes -> bounded recovery -> sensitive content classification -> scoped report`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
