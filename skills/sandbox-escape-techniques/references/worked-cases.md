# Worked case: language evaluation still cannot open the protected resource

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied sandbox result.

```text
policy: arithmetic allowed; resource outside /owned forbidden
owned expression evaluates to expected marker
attempted protected open -> denied by supplied filesystem broker
no outside bytes or authority returned
local /owned resource control succeeds
```

**First approach and failure.** Calling successful code evaluation an escape skipped the resource policy that defines the boundary.

**Revised approach.** Trace the open operation into the broker denial. Evaluation capability exists, but the requested outside-resource edge remains blocked.

**Independent controls.** The owned resource control rules out a universally broken file interface. Keep language restrictions and broker authority as separate layers.

**Completed result and limits.** No outside-resource escape in this trace. Other processes, syscalls, objects and actual sandbox implementations require independent review.
