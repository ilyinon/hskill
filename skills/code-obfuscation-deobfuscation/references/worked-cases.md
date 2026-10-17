# Worked case: integer algebra loses an eight-bit wraparound branch

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Correct a supplied simplification while preserving its specified behavior.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** The integer claim x+1 is always greater ignored the stated machine-width overflow.

**Revised approach.** Retain the wrap case or simplify to x==255 under this exact unsigned contract. Compare outputs at the boundary before removing the branch.

**Independent controls.** Exhaustively check x=0..255 in the teaching model; include 254 and 255 as discriminating controls. Side effects outside the predicate need their own preservation checks.

**Completed result and limits.** The corrected predicate is equivalent under the supplied 8-bit model. This is not proof about arbitrary compiler overflow rules or a complete binary deobfuscation.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_unsigned_predicate_matches_every_byte`. This is not a product/runtime exploit test.
