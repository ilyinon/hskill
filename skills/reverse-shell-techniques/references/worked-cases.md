# Worked case: the marker already completes the requested proof

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Decide the next useful action from an authorized local-execution observation.

```text
user task: show local owned execution marker only; no remote session requested
supplied lab trace: owned marker emitted by expected test identity
proposed listener on a different host is outside the allowed connection list
no remote session evidence supplied
```

**First approach and failure.** Opening a remote-shell recipe adds a new connection goal after the requested proof is already sufficient.

**Revised approach.** Preserve the attributable marker, identity and trace. Complete the requested local proof without requiring a remote session.

**Independent controls.** Compare marker nonce and process identity with the expected lab record; a generic listener connection would not validate this identity anyway.

**Completed result and limits.** The local requested proof is complete. No remote session, persistence or wider network authority is established or needed.
