# Worked case: an empty UI still exposes a job workflow in captured traffic

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Map the supplied app evidence and select the next useful review.

```text
scope=app.example.invalid only; member session in tenant=A
UI: empty exports list
captured POST /exports -> {job: a7}
client code polls GET /exports/{job}/result
bundle also mentions metrics.other.invalid; no permission for that host
```

**First approach and failure.** Concluding there are no exports from an empty UI lost the observed creation and polling edges.

**Revised approach.** Record the member-to-export-to-job-to-result graph with provenance. The next useful review is result authorization and tenant binding, not a general directory spray.

**Independent controls.** Mark the result fetch as unobserved and the metrics host as out of active scope. The creation capture independently establishes that the job workflow exists.

**Completed result and limits.** A bounded attack-surface inventory and precise handoff are complete. No result leak or authorization failure has yet been shown.
