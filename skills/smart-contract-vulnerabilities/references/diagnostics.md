# smart-contract-vulnerabilities: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Exact deployed semantics and role state | Pin compiler/bytecode, proxy layout, chain state and caller permissions. |
| Call ordering and final invariant | Trace state changes, external calls, callbacks, revert behavior and settled balances. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| External call is present | Reachable reentrancy effect or protected checks/effects ordering | Inspect the callback's observed state and subsequent permission decision. |
| Nested call happens | Reentry, not necessarily excess transfer | Compare total committed value with the original entitlement. |

## Interpret failure and finish the task

A pattern match or reverted transaction is not a committed exploit. Arithmetic, delegatecall and signature recipes require their own deployment prerequisites.

Track `caller entitlement -> state update/call order -> callback state -> committed transfer/state -> invariant`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
