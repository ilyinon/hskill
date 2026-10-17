# Worked case: the early exit comes from missing input, not debugger state

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose two supplied traces before patching a binary.

```text
normal run: config present, debug flag=0 -> reaches owned computation marker
debug run: config path wrong, debug flag=0 -> exits at missing-config branch
controlled debug run with same config -> reaches same marker
no debug-dependent branch difference supplied
```

**First approach and failure.** Labeling every debugger-only failure anti-debugging skipped the changed configuration input.

**Revised approach.** Compare the first divergence and restore the same input configuration. The supplied countercontrol reaches the intended behavior without altering a detection branch.

**Independent controls.** Keep binary hash, working directory, inputs and debug flag explicit. A successful matched-input run explains this failure, not every possible anti-analysis layer.

**Completed result and limits.** This failure is diagnosed as setup/input mismatch. No anti-debug bypass or universal absence of detectors is claimed.
