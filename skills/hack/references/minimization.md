# Reduce a working reproducer without losing its meaning

Use after a result is reproducible and a smaller case would clarify the cause,
support a fix, or make review easier. Preserve the original input and raw results.
Minimization is unnecessary when the existing proof is already sufficient.

Define a three-way predicate before deleting anything:

```text
interesting: the same boundary/effect occurs under the required identity and state
not-interesting: the valid operation ran, but that effect did not occur
unknown: setup failed, a prerequisite vanished, the tool timed out, or evidence is missing
```

Keep a discriminating control: legitimate behavior still works, or changing the
suspected causal feature removes the effect. “Same status code” is rarely a
sufficient predicate. For source-only work, retain the reachable data path and
missing-control evidence rather than inventing an executable effect.

Reduce one dimension at a time: sequence steps, fields, input length, encoding
layers, object count, or concurrency. Try removing groups first; keep a reduction
only after the interesting predicate and its control still hold. Revisit the
remaining individual elements if needed. A greedy reduction may be 1-minimal
under the tested deletions; it is not necessarily globally smallest.

Keep causal prerequisites. Removing authentication, tenant binding, a preceding
state transition, allocator history, a packet fragment, or a relevant timing
window can turn a valid proof into a different phenomenon. Reset independent
trials to equivalent state; do not compare a fresh baseline with a mutated case.
For races, repeat bounded paired trials and retain uncertainty when outcomes are
too noisy. Never convert an unknown into a negative to speed up shrinking.

Example: a callback sequence contains logging, two delivery attempts, and two
distinct legitimate partial refunds. Remove logging, then isolate an identical
delivery repeated for the same operation. Compare that with one delivery and
with two different operations. A fix should reject the repeated delivery while
preserving the allowed partial operations. Simply rejecting every second callback
would fit the bad trace but violate the legitimate case.

Stop when the remaining case explains the mechanism, the agreed budget is used,
or further trials would exceed authorization. Report what was removed, the
retained effect and control, tested reset conditions, and any remaining noise.
Do not run a generic minimizer against a live destructive operation.
