# Try to disprove a consequential conclusion

Use for a complex, surprising, or high-impact result, or when the proposed repair
depends on a subtle causal explanation. A separate pass is useful; a separate
agent is optional when available and authorized. Routine clear results do not
need a second workflow.

Start with the strongest plausible alternative that would change the conclusion:
an administrator's session, a different tenant, a cached response, a retry, an
already-enforced defense, a stale build, measurement noise, or a parser artifact.
Prefer alternatives supported by the task's evidence over an exhaustive list.

Return to original requests, bytes, source paths, or event records. State what
the proposed explanation and its alternative predict differently, then choose
the smallest permitted discriminating check. A second scan reporting the same
label, or a second agent reading only the first agent's summary, is not an
independent check.

Example: repeated events suggest a double refund. The strongest alternative is
two valid partial operations. Compare stable operation IDs, delivery IDs, amounts,
and ledger deltas. One callback repeated for the same operation, two distinct
operations, and a failed transport attempt have different implications. State
which evidence distinguishes them; do not treat event count alone as the defect.

If delegating an independent check, provide the user's task, scope, and minimum
raw artifacts. Ask for an assessment from those artifacts before sharing your
preferred conclusion or patch. Preserve both results and resolve disagreements
with discriminating evidence. Do not start external actions or messages merely
because a reviewer suggests them.

Outcome choices:

- **Survives the check:** state the alternative tested, evidence, and bounded
  conclusion. One refutation attempt does not rule out every explanation.
- **Refuted or narrowed:** revise the claim and any downstream impact or repair.
  Preserve useful observations rather than defending the first interpretation.
- **Unresolved:** state the competing explanations and the missing observation.
  Do not average incompatible conclusions or select the more dramatic result.

For a fix, also challenge its specificity: does it address the failed invariant
and retain a legitimate near-neighbor case, or just block the published input?
