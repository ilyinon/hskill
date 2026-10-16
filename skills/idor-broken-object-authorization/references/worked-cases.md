# Worked case: protected parent, unbound attachment

Synthetic owned-account exercise: [input](./examples/input.json), [model](./examples/model.py).

**Goal.** Assess the attachment handler, then repair a demonstrated object-policy defect.

**First approach.** Alice/A selects Bob's parent `pB`. It returns 403, correctly enforcing the parent rule. That result does not exercise a mismatched child under Alice's permitted `pA`.

**Revised approach.** Read the handler: after authorizing `parent_id`, it fetches `children[attachment_id]` independently. Keep Alice/A and `pA` fixed; change only `cA` to the owned Bob fixture's `cB`. The response is 200 with `bob fixture`, despite `cB.parent == pB`.

**Controls and repair.** Alice/pA/cA succeeds. Alice/pB/cB is denied. Bob/pB/cB succeeds. Enabling `bind_child=True` denies Alice/pA/cB without breaking either owner baseline. `test_solving_examples.SolvingExamples.test_authorized_parent_does_not_authorize_foreign_child` verifies bodies and denials, not just status.

**Completed result.** An authenticated cross-parent private-child read and the missing binding check. The parent 403 was a useful local negative control, not a reason to abandon the entire authorization class. No other user's data, enumeration, write capability, or deployed service is involved.
