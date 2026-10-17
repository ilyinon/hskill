# Worked case: an absent alert coincides with an unhealthy collector

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret supplied benign-test telemetry without changing protections.

```text
benign test process reports completed owned marker
alert dashboard shows no event for it
collector heartbeat absent for the whole test interval
known-good benign canary event is also missing
no independent endpoint telemetry supplied
```

**First approach and failure.** Calling the missing alert an undetected technique ignored that collection health was not established.

**Revised approach.** Classify alert visibility as unknown and restore/verify the collector in the authorized test environment before interpreting control coverage.

**Independent controls.** A healthy interval with a known-good canary is required to distinguish collection failure from a control-specific result. Execution evidence remains separate from telemetry.

**Completed result and limits.** Only the benign local marker is supported; evasion or invisibility is not. No payload, sensor bypass or protection change is provided by this case.
