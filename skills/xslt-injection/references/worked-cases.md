# Worked case: the transform runs but its external document resolver denies

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound an offline transform trace.

```text
user controls stylesheet in an authorized teaching transform
local arithmetic/text transform -> expected marker
external document reference -> resolver denial before network; fetch count=0
extensions disabled; no extension call trace
policy: transformations allowed, external resources forbidden
```

**First approach and failure.** Calling a vendor string or successful stylesheet an external-read/RCE proof skipped the resource gate.

**Revised approach.** Trace the valid transform to the resolver rejection. The supplied external-resource candidate is blocked even though stylesheet evaluation works.

**Independent controls.** A valid local transform rules out a broken harness; compare denial provenance and fetch count. Extension permission remains a separate fact.

**Completed result and limits.** No external read or execution is demonstrated by this trace. Other processor versions, XML entry parsing and output resolvers require separate review.
