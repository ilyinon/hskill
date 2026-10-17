# ghost-bits-cast-attack: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Concrete representation mismatch | Locate the exact narrowing, permissive decoder or validation/use normalization path. |
| Same input at validation and sink | Record code point, encoded bytes and actual consumed byte sequence. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Code point has a dangerous low byte | Narrowing produces that byte or a real encoding preserves the character | Trace the conversion call, not the numeric coincidence. |
| Filter misses a character | Only a matcher difference or downstream syntax effect | Inspect emitted bytes and a reachable parser boundary. |

## Interpret failure and finish the task

A WAF acceptance is not downstream control. A patched version or CVE label alone does not establish a reachable mismatch; ordinary UTF-8 is not Java byte-cast truncation.

Track `validated representation -> actual conversion -> downstream bytes -> parser interpretation -> bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
