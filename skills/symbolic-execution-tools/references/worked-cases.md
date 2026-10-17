# Worked case: integer arithmetic produces an input outside the byte domain

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Solve and independently verify the supplied finite arithmetic task.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** The negative integer satisfies the wrong model but cannot be transported as the specified input byte.

**Revised approach.** Use the original byte-width relation and bounds: x=242 gives 259 mod256=3. Reject -14 as outside the input domain before evaluating acceptance.

**Independent controls.** Enumerate the 256 valid bytes or use independent modular arithmetic; exactly one input works. x=241 fails, and a congruent value outside the byte range is not accepted input.

**Completed result and limits.** The recovered byte is 242 under the complete supplied predicate. No native binary, angr integration or omitted program state is claimed to be validated.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_original_finite_word_equation`. This is not a product/runtime exploit test.
