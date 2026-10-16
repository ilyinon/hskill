# Worked case: first-hop allowlist, second-hop escape

This is a synthetic offline case. [Input](./examples/input.json) and [complete model](./examples/model.py) use supplied response records; no HTTP request is made.

**Goal.** Establish whether preview stays on `docs.example.invalid`, then fix the demonstrated failure. Only the supplied model is in scope.

**First approach.** Submit the direct control `https://other.example.invalid/result`. It is denied. This establishes the initial host check, not the destination of a redirected fetch.

**Why the approach was insufficient.** Reading `preview` shows validation occurs only when `hop == 0`. The supplied allowed `/start` response redirects to the foreign `/result`. No DNS trick or metadata request is needed to exercise this path.

**Revised approach.** Trace the allowed start URL through the supplied responses. With `validate_each_hop=False`, the trace contains both URLs and returns `owned-fixture-marker`. The forbidden destination is reached under the declared policy. The same input with `validate_each_hop=True` is denied before the second URL enters the trace.

**Independent check.** Compare the final result and the attempted-destination trace, not just status. Preserve an allowed terminal URL as a positive control and the direct foreign URL as a negative control. `test_solving_examples.SolvingExamples.test_redirect_policy_at_each_hop` exercises these three paths.

**Completed result.** A demonstrated redirect-policy defect and a bounded fix for this model. Internal reachability, credential retrieval, deployed HTTP behavior, DNS rebinding, and production parser completeness remain untested. The successful local proof meets this task; adding a metadata chain would not strengthen its conclusion.
