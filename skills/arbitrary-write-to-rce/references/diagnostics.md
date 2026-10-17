# arbitrary-write-to-rce: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Write contract | Measure width, alignment, address/value control, repetition and required existing bytes. |
| Reachable target and trigger | Pin actual mappings/runtime, integrity checks and the event that consumes the modified value. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A controlled write succeeds | Only a primitive or the complete intended target value | Compare all target bytes after the write. |
| A historical hook exists in notes | Absent/unused/protected target on this build | Inspect the actual consumer and trigger before selecting a target. |

## Interpret failure and finish the task

A write fault is not execution; a low-byte change is not a full-width pointer replacement. Missing target or trigger prerequisites require a different supported hypothesis, not repeating the same overwrite.

Track `write primitive -> exact final target bytes -> reachable consumer/trigger -> bounded observed effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
