# path-traversal-lfi: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Final path semantics | Record decoding, canonicalization, root relation, symlinks and open/include operation. |
| Read versus interpretation | Identify whether selected bytes are returned as data or executed by an include handler. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| String starts with the root text | True path containment or sibling-prefix collision | Compare canonical path components/ancestry, not string prefixes. |
| Traversal spelling is rejected | Correct policy or another canonical route remains | Check the final resolved path used by the open call. |

## Interpret failure and finish the task

A nonexistent file error proves neither disclosure nor containment. A legitimate out-of-root denial closes only that tested path; symlink/race behavior requires actual resolution semantics.

Track `input -> decoded/joined path -> resolved containment -> actual open/include -> recovered bytes or effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
