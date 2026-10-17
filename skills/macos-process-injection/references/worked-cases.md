# Worked case: the controlled environment variable never reaches the target

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret the supplied protected-launch trace.

```text
test shell contains a loader-related variable
supplied launcher contract removes that variable before target creation
target environment snapshot lacks it; loader opens only configured signed dependency
no foreign library or marker is loaded
```

**First approach and failure.** Calling the shell environment an injection primitive skipped the launcher boundary.

**Revised approach.** Trace the environment into the actual target and inspect loaded dependency evidence. The proposed variable path is absent in this launch contract.

**Independent controls.** A separate unprotected teaching launch that preserves the variable would be a different configuration, not proof against this target.

**Completed result and limits.** No target-process injection in the supplied trace. Actual macOS builds, signing exceptions, XPC endpoints and memory permissions require independent review.
