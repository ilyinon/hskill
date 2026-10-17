# Work backward from the requested result

Use when several promising routes compete or intermediate successes do not yet
produce the deliverable. Start with the user's observable completion criterion,
then ask what must be true immediately before it can hold.

```text
goal: current object bytes accepted by the supplied offline verifier
requires ALL: exact bytes + matching object/version + verifier's acceptance rule
bytes: route A = old export; route B = current ordered fragments
route A: incompatible version; retain as historical evidence
route B: first fragment known, continuation unknown
acceptance rule: known from current manifest
next useful action: obtain that continuation within the existing scope
```

Separate **all required conditions** from **alternative ways** to establish a
condition. A route satisfying only one required condition does not complete the
goal. An unavailable preferred method does not disprove an alternative route.
Attach evidence or unknown to the necessary joins; use
[edge contracts](chain-contracts.md) for identity, state, and representation.

Expand only the dependency frontier needed for a plausible route. Prefer a small
check that can establish or eliminate a necessary condition over an impressive
capability with no supported path to the goal. Cost estimates are rough choices,
not invented probabilities. Do not enumerate every possible technique.

Keep a branch's failed prerequisite and its conditions. Revisit it when new
evidence changes that prerequisite, not merely because another branch is hard.
If expansion cycles back to the same unresolved claim, expose the circular
assumption and find an independent source. Do not use the desired conclusion as
its own prerequisite evidence.

Join backward requirements with established forward capabilities, then perform
the earliest useful unresolved step. A proposed route is still a hypothesis;
verify the actual deliverable under the supplied construction. Preserve the
current environment and authorization: a route requiring new access or a
prohibited effect is not made feasible by drawing it in a plan.

Stop expanding when the requested criterion is met or every supported route has
a concrete blocker. For a partial result, identify the nearest missing necessary
condition, available alternatives, and what evidence would unblock it. In an
audit the deliverable may be a source-level proof; do not silently redefine it as
live execution or a longer impact chain.
