# defi-attack-patterns: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Pinned economic construction | Record chain/fork state, exact contracts/oracle window, token units and actor permissions. |
| Full balance accounting | Include principal repayment, fees, slippage, gas and outstanding obligations once each. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Spot price changes | Market movement, not a usable oracle decision or profit | Trace the actual valuation window and consuming transaction. |
| Intermediate balance increases | Loan proceeds, unsettled costs or net gain | Compare final owned balances after all obligations. |

## Interpret failure and finish the task

A reverted local transaction does not establish a committed economic effect. Flash liquidity and a gross gain are intermediates, not by themselves a profitable invariant violation.

Track `permitted capital/state -> reachable market/oracle change -> consuming action -> repayment/cost settlement -> net invariant result`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
