# Check how a conclusion changes with its input

Use when a fix or model could fit one example accidentally, or a full independent
oracle is unavailable. Derive a relation from the actual contract before changing
the data; a transformation is not harmless merely because it looks cosmetic.

| Contract condition | Transformation | Expected relation |
|---|---|---|
| Object-field order has no semantic meaning | Serialize the same fields in a different order | Same result and boundary decision. |
| IDs are opaque and compared only for equality | Rename IDs bijectively in input, policy and references | Same effects after mapping names back. |
| Logs/failed transport attempts do not mutate state | Insert those events | Same ledger effect, though event locations change. |
| Independent operations commute under the tested policy | Permute their order | Same per-operation effects; do not assume this for dependent operations. |
| A completed operation may apply once | Add another delivery for that operation | Same credit under the intended policy. |
| Different authorized partial operations may both complete | Replace the repeated operation with a distinct authorized one | Both legitimate credits remain possible. |

The last two are deliberately different obligations. A repair that makes both
cases behave identically can be overbroad. For access control, changing owner or
tenant is usually a meaningful change; preserve expected denial/allowance from
the policy rather than requiring invariance.

Use equivalent reset state and retain the original input. Record the relation,
its prerequisites, transformed input, and observed effect. If the transformation
changes a prerequisite, classify that trial separately. A tool failure leaves the
relation untested. For noisy concurrent behavior, use bounded paired trials and
report uncertainty rather than a deterministic rule.

The repository's `test_reasoning_models.py` exercises field order, opaque-ID
renaming, non-mutating events, commuting operations, retries and legitimate
partials on the [reviewed ledger](../scripts/hack_ledger_model.py). Fixed-seed
generated traces supplement explicit boundary cases. These relations check the
teaching model; production semantics still need their own evidence.

Passing many related examples is not an independent proof if all expectations
come from the same mistaken abstraction. Include a concrete observed baseline
and at least one control that would fail a plausible incorrect repair.
