# Worked case: the bit order determines the recovered bytes

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Recover an inert marker from a supplied single-channel byte model.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Treating the sample bytes as plain text finds only repeated d/e characters; reversing each bit group produces the wrong bytes.

**Revised approach.** Extract low bits in the stated order: 01001111 01001011 -> 4F 4B -> OK. Check length2 and byte sum79+75=154.

**Independent controls.** Reconstruct the bit groups from recovered bytes and compare all16 samples' low bits; flipping the first low bit fails the checksum.

**Completed result and limits.** The marker is OK under this complete bit-channel contract. No inference about arbitrary image steganography, hidden intent or unknown payloads follows.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_lsb_recovery_and_corruption_control`. This is not a product/runtime exploit test.
