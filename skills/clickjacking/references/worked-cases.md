# Worked case: a frameable page still requires fresh verification

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret the supplied isolated UI-action trace.

```text
settings page is frameable; test user session is present
inert local UI test clicks protected setting action
server requires fresh verification token not available in frame
response=verification required; setting remains old
valid owned verification flow changes setting to new
```

**First approach and failure.** Calling frameability a completed setting-change exploit ignored the final verification gate.

**Revised approach.** Trace the framed interaction to the denied action and unchanged state. Frameability is established; the requested protected change is not.

**Independent controls.** The valid verified action establishes the operation and independent state snapshot. Do not generalize one protected action to all page controls.

**Completed result and limits.** No protected setting change in this trace. Frame-policy hardening can still be appropriate, but a different action needs its own browser-feasible proof.
