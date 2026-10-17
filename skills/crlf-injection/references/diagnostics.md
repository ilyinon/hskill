# crlf-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Representation at every stage | Record encoded input, actual decoding, character narrowing and final wire bytes. |
| Downstream parser | Inspect whether a new HTTP field/message or log record is parsed, not just rendered. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Percent escapes appear in a value | Literal text or later decoding | Inspect the exact consumer representation. |
| A Unicode character has a low control byte | A narrowing conversion exists or normal UTF-8 preserves it | Locate a concrete conversion before inferring a newline. |

## Interpret failure and finish the task

A rejected header setter is a control for that path, not universal parser safety. UTF-8 decoding alone does not turn arbitrary Unicode characters into ASCII CR/LF.

Track `input representation -> transformations -> emitted bytes -> parsed field/record -> separately supported impact`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
