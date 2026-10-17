# Worked case: two conversion contracts produce different bytes

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Distinguish narrowing from UTF-8 without running a service.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Using the low byte of the code point as the emitted byte assumed conversion A without evidence.

**Revised approach.** Trace the actual encoder and compare both representations. Under B, the emitted sequence contains no CR byte 0D; the proposed narrowing mechanism does not apply.

**Independent controls.** Compute both byte sequences independently; a genuine low-byte cast would be a different source path. Even A would need a reachable sensitive parser before claiming impact.

**Completed result and limits.** No narrowing-based newline injection on the supplied UTF-8 path. No vendor component, patched CVE or live parser has been tested.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_charset_encoding_is_not_low_byte_narrowing`. This is not a product/runtime exploit test.
