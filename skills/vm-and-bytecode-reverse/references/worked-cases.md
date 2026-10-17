# Worked case: the immediate is little-endian

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Correct a miniature VM decoder from two independent trace points.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Changing later arithmetic to force the final result would conceal the first decoding mismatch.

**Revised approach.** Fix LOAD16 byte order. The same decoder yields 1 then 258 for the original input and 2 then 259 for the control.

**Independent controls.** Check operand consumption/PC advance and both trace points, not only the desired final value. No actual bytecode is executed outside the defined teaching operations.

**Completed result and limits.** The corrected operand semantics match the supplied traces. Other opcodes, branches and a full native challenge remain unvalidated.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_vm_operand_byte_order_against_trace`. This is not a product/runtime exploit test.
