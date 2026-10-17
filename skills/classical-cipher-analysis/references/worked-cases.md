# Worked case: a readable fragment loses to a full-message check

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Recover a supplied uppercase rotation message with an independent checksum.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Choosing a candidate from a plausible two-letter fragment leaves many rotations possible.

**Revised approach.** Enumerate the 26 rotations, test the full byte sum, then re-encrypt. HELLO has sum372 and rotating forward3 reproduces KHOOR.

**Independent controls.** Check every rotation rather than only the favored candidate; a changed ciphertext character must not pass both re-encryption and the original independent record.

**Completed result and limits.** The plaintext and rotation are recovered for this supplied toy construction. No cryptographic security or unique recovery for arbitrary short strings is implied.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_rotation_and_independent_checksum`. This is not a product/runtime exploit test.
