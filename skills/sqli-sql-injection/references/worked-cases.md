# Worked case: a protected value hides an unsafe ordering expression

Synthetic local SQLite exercise: [input](./examples/input.json), [model](./examples/model.py). The database contains only three fictional names and creation-order numbers.

**Goal.** Review the complete query path and fix any input-to-SQL boundary error.

**First approach.** A quote/boolean string is placed in `term`. It returns no rows. The source binds term through `LIKE ?`, so the string is data; this attempt neither finds injection there nor establishes safety of `sort`.

**Revised hypothesis.** `sort` is concatenated after `ORDER BY`. Policy allows only `name` and `created`. First confirm `sort=name` gives `anna, bo, zoe`. Then use the syntactically valid SQLite ordering expression `length(name), name`: the result is `bo, zoe, anna`. This controlled change locates raw SQL structure control in sorting. It does not demonstrate unauthorized row access, extraction, or execution.

**Fix and verification.** Map a finite set of public sort names to fixed SQL fragments. With `restrict_sort=True`, the expression is rejected while the two supported sorts still work and term remains bound. `test_solving_examples.SolvingExamples.test_bound_value_and_raw_sort_are_separate` runs the actual in-memory SQLite queries and both controls.

**Completed result.** A reproducible query-construction defect with bounded impact and a regression-checked fix. Error text alone was not the proof. Stopping after the unsuccessful term probe would have missed a separate component of the same statement.
