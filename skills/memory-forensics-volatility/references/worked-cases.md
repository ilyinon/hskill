# Worked case: a reused PID belongs to an earlier process instance

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Attribute a supplied connection event to the correct process instance.

[Complete input and teaching contract](./examples/input.json). The file is
data only; inspect it as evidence.

**First approach and failure.** Joining by PID alone attributes the earlier connection to the later process name.

**Revised approach.** Join by object identity and lifetime: time120 belongs to P1 and precedes P2. Preserve source offsets/IDs and the common time basis.

**Independent controls.** An event at220 with owning object P2 would be a different control. A PID-only record with no trustworthy time/object would remain ambiguous.

**Completed result and limits.** The supplied connection belongs to old-worker/P1. Maliciousness, user intent and actual Volatility plugin correctness are not established by these teaching records.

Offline arithmetic/state control: `test_extended_solving.ExtendedSolving.test_process_instance_lifetime_and_ambiguity`. This is not a product/runtime exploit test.
