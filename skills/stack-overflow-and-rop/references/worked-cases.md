# Worked case: correct control and argument, wrong entry alignment

Synthetic stack-accounting exercise: [input](./examples/input.json), [bounded checker](./examples/model.py). No binary is executed, and the checker is not an emulator.

**Goal.** Repair the supplied abstract marker call. Addresses, offset 40, initial saved-RIP slot 40968, expected argument 4660, and required target-entry `RSP % 16 == 8` are given facts of this exercise.

**First approach.** The words are `[pop_rdi_ret, 4660, marker]`. Both target and argument are correct. Changing the overwrite offset because the marker fails would discard an already established primitive.

**Diagnosis.** Count consumed words: the first return consumes one, the pop consumes one, and the gadget's return consumes one. The marker sees `(40968 + 24) % 16 == 0`, violating the supplied contract.

**Revised chain.** Prepend one plain ret. Four words are consumed before marker entry, so `(40968 + 32) % 16 == 8`, with the same argument. `test_solving_examples.SolvingExamples.test_stack_contract_uses_actual_initial_position` checks the initial failure and repaired marker result.

**Counterexample.** After a different pivot with saved-RIP slot 40960, the original three-word chain is already aligned; adding ret breaks it. The same test verifies this opposite result. The useful rule is state accounting, not always adding a gadget.

**Completed result.** A verified correction under the supplied AMD64-like abstract contract. Actual mappings, gadget bytes, process protections, stack writes, function side effects, and remote success remain untested. Applying this to a real target requires those independent prerequisites.
