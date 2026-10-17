# hash-attack-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact construction, not just digest | Read key placement, HMAC use, message encoding and verification routine. |
| Claimed cryptographic property | Separate collision, preimage, length extension, guessing and timing evidence. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Digest size resembles SHA-256 | Algorithm clue, not whether it is keyed-prefix or HMAC | Inspect construction and accepted baseline. |
| Length-extension tool outputs a candidate | Syntactically generated value or verifier-accepted forgery | Check the original verification predicate and construction assumptions. |

## Interpret failure and finish the task

A parser/tool failure did not test integrity. A collision does not establish preimage recovery or HMAC forgery; a single timing sample is not a reliable oracle.

Track `exact hash/MAC construction -> applicable property -> candidate -> original verifier -> bounded integrity/recovery result`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
