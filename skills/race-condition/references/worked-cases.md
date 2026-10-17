# Worked case: two checks observe the same unused voucher

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose a supplied bounded interleaving and propose an invariant-preserving repair.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Counting success responses alone would not distinguish this from retries; the interleaving and final sum do.

**Revised approach.** Locate the shared check/credit boundary and make consumption plus ledger effect atomic with the appropriate transaction/conditional-update design.

**Independent controls.** Only one concurrent operation may commit the credit; sequential retry stays harmless and a different voucher can still be used. Verify durable sum, not only a boolean flag.

**Completed result and limits.** A race exists in the supplied state-machine trace. This is not a real database isolation benchmark or permission for financial traffic.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_interleaving_and_atomic_consumption`. This is not a product/runtime exploit test.
