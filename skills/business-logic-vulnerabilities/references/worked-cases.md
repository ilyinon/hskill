# Worked case: idempotent retries, duplicate full refund

Synthetic integer-credit ledger: [input](./examples/input.json), [model](./examples/model.py). There is no payment provider or real money.

**Goal.** Test the rule: one full refund per order and total credited no greater than the paid 100 cents.

**First approach.** Call with `request-1`, then retry `request-1`. Both report a cached result and the ledger remains 100. Request idempotency is working; the business operation may still be repeatable with a new request identity.

**Revised approach.** Keep the same owned order and call `request-2`. The broken model keys the ledger by request ID, so total credited becomes 200. The failure is sequential business-operation deduplication, not a demonstrated race.

**Repair.** Deduplicate the full-refund operation by `full-refund:<order-id>`, retaining request-result caching for retries. In the fixed model, all three supplied calls leave total credit at 100. A different owned order can still receive its own full refund.

**Independent check.** `test_solving_examples.SolvingExamples.test_request_idempotency_and_business_uniqueness` checks both the sequence's final sum and a second order. Counting two success responses would have missed the distinction.

**Completed result.** The full-refund invariant is repaired for this sequential model. Partial refunds, transaction isolation, external delivery, and concurrent atomicity need their own contracts and tests; a universal one-operation key would be wrong for some of them.
