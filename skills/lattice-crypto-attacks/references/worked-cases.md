# Worked case: the short-vector candidate fails the original congruence

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Choose the valid bounded candidate from supplied solver outputs.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Calling x=2 recovered because reduction completed ignored that 2^2-5 is not divisible by11.

**Revised approach.** Check original constraints: 4^2-5=11, 4 is in range and 4 mod3=1. Root7 fails the range even though it satisfies the congruence.

**Independent controls.** Enumerate the six allowed values as an independent teaching check. This validates the selected candidate, not an unprovided lattice construction.

**Completed result and limits.** The bounded unknown is4 for these inputs. No LLL implementation, general Coppersmith bound or real key recovery is certified.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_candidates_against_original_algebra`. This is not a product/runtime exploit test.
