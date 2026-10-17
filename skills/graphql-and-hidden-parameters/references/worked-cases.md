# Worked case: a nested resolver loses the tenant constraint

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Finish an audit after introspection denial using the supplied resolver trace.

```text
introspection -> denied
principal=test-a tenant=A; project(id=a1) authorized
attachment resolver uses args.fileId globally, ignoring project relation
query project(a1).attachment(fileId=b1) returns marker=B-private
policy: private attachment inherits actual project tenant
```

**First approach and failure.** Concluding no finding from introspection denial confuses schema discovery with the already supplied resolver path.

**Revised approach.** Trace the child lookup and constrain attachment to the authorized project/tenant before returning its body. Keep the query and requesting identity fixed.

**Independent controls.** Own attachment succeeds, foreign-parent request denies, and own parent plus foreign attachment must deny after repair. Schema visibility is not a prerequisite for this source proof.

**Completed result and limits.** A nested private-read flaw is supported in the supplied model. Batching, query-cost limits, writes and other resolvers remain untested.
