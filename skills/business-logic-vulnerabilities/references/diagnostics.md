# Business logic: identify the invariant and the operation identity

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Actors, object state, and intended transition | Write the normal state transition and its server-side invariant, including units and rounding. |
| Request identity versus business operation | Determine which key deduplicates transport retries and which object/action must occur once. |
| Final durable effect | Compare ledger/state snapshots, not only a success message or UI. |
| Sequential versus concurrent behavior | Reproduce sequential logic first; call a race only with a demonstrated interleaving. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Same request key retries harmlessly | Request-level idempotency works | Inspect whether a new key can repeat the same forbidden business operation. |
| Two operations succeed | Legitimate partial operations or a value/state violation | Sum final effects against the declared paid/quota/state invariant. Count server effects, not responses. |
| UI step cannot be skipped | Frontend routing or server enforcement | Trace the backend transition predicate and an authorized alternate entry path. |
| Concurrent test has inconsistent counts | Client retries, partial failure, or a race | Correlate operation IDs and durable effects; isolate ordering before attributing a race. |
| New business-key guard rejects everything | Overly broad key may prohibit legitimate partial operations | Recheck the domain contract; full-refund and partial-refund models require different invariants. |

A request error is not evidence of a protected business invariant unless the intended operation and final state were examined.

## Close the requested task

Track `actor → allowed state → operation identity → state/value change → invariant`. For the supplied fixture, integer credits are sufficient; do not create real charges. A fix must preserve valid operations and reject the violating sequence. Sequential proof does not validate atomicity under concurrency, external-provider rollback, or retry delivery semantics.
