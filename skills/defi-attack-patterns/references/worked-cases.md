# Worked case: the gross gain disappears after the outstanding fee

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Compute the supported economic result from a complete integer teaching ledger.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Calling the intermediate +2 a profit omitted the remaining fee.

**Revised approach.** Settle the fee once: final balance=99, net change=-1. Do not subtract the already repaid principal again.

**Independent controls.** Reconcile all ledger entries and units; a separate control with no outstanding fee would have a different result. Price movement alone does not determine the final balance.

**Completed result and limits.** No positive profit under this supplied ledger. This says nothing about a real protocol's invariant, oracle manipulation or deployed transactions; no chain was contacted.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_settled_net_balance_without_double_count`. This is not a product/runtime exploit test.
