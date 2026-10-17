# Worked case: the executable text mapping does not make the writable buffer executable

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret supplied mapping and transfer records.

```text
program text mapping=read+execute
controlled data buffer mapping=read+write, execution denied by supplied runtime policy
attempted transfer to buffer -> execution fault before marker
normal text function -> owned marker
no alternative executable target chain supplied
```

**First approach and failure.** Calling an executable text mapping an NX bypass confused code pages with the controlled writable buffer.

**Revised approach.** Compare the exact transfer address with runtime permissions. The controlled buffer remains non-executable under this trace.

**Independent controls.** The normal function marker verifies ordinary execution; the buffer fault verifies this failed transfer, not every possible chain.

**Completed result and limits.** No executable-data or control-flow bypass is established. Other mitigations and primitives require their own build-specific evidence.
