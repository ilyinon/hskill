# race-condition: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Invariant and sequential baseline | Define committed state/value and normal idempotent behavior on owned objects. |
| Actual interleaving | Correlate transaction/operation IDs with reads, checks, writes and commits. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Several responses say success | Cached retry, distinct allowed actions, or duplicate durable effect | Inspect ledger/state and unique operation identities. |
| Sequential test passes, overlapping test fails | A check/use or isolation gap may matter | Locate both checks relative to the protected commit. |

## Interpret failure and finish the task

A client scheduling failure did not test overlap. A sequential violation is a domain-logic bug even without a race; do not infer concurrency from timestamps alone.

Track `shared state -> overlapping checks -> committed effects -> violated invariant -> atomic repair and controls`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
