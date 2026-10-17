# Worked case: two writable bytes cannot change an incompatible upper half

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Check whether a supplied primitive can reach the requested abstract marker target.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Treating arbitrary low-half value control as full-word control ignored the unchanged high half.

**Revised approach.** Compute the complete post-write word. The requested marker is unreachable with this primitive and initial state; preserve the partial capability and missing prerequisite.

**Independent controls.** For a different supplied target 0x12340099 the same low-half write would suffice. That arithmetic control does not establish a real control-flow consumer.

**Completed result and limits.** The stated abstract target is inapplicable; no RCE chain is established. Real memory mappings, pointer integrity and execution require independent evidence.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_partial_write_preserves_upper_bits`. This is not a product/runtime exploit test.
