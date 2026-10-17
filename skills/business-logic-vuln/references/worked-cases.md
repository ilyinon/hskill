# Worked case: a refund sequence needs an accounting invariant

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Choose the correct branch for sequential partial-refund evidence.

```text
paid=100 integer cents; multiple partial refunds allowed
request r1 credits 60; same r1 replay adds 0
fresh r2 credits 60; ledger total=120
no concurrent interleaving supplied
```

**First approach and failure.** Classifying the two request IDs as a race or forbidding every second refund contradicts the sequential trace and partial-refund policy.

**Revised approach.** Route to business-logic diagnostics. Enforce cumulative credited amount plus the next amount <= paid while preserving idempotency.

**Independent controls.** The repair must permit 60+40 and keep same-ID retries harmless. Atomic enforcement is a requirement if concurrency is introduced, not a demonstrated race here.

**Completed result and limits.** The accounting flaw and focused repair are supported. Actual provider transactions and concurrent behavior remain outside the teaching case.
