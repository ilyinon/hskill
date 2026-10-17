# Worked case: internal expansion works while external resolution is disabled

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess the supplied parser configuration and observations.

```text
parser contract: internal entities enabled, external resource resolver denies all
valid internal marker expands -> OWNED
external entity test -> explicit resolver denial, resource opens=0
source has no later XInclude or stylesheet stage
policy: no external files/network
```

**First approach and failure.** Inferring external-entity access from an internal expansion skipped the independently controlled resolver.

**Revised approach.** Correlate successful parsing and the explicit external denial. The attempted external resource was not opened under this complete path.

**Independent controls.** Preserve the internal entity as the valid parser baseline and a literal XML value as a data control. Do not invent later stages absent from source.

**Completed result and limits.** No external-resource violation on this path. Real parser versions and other XML consumers remain outside this synthetic configuration review.
