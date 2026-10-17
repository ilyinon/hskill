# Worked case: the accepted key is limited to a fixed status action

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied SSH trust trace.

```text
owned test key authenticates test-a to permitted host
supplied destination contract binds this key to fixed status action
requested arbitrary command -> denied/replaced by status response
observed response=owned status marker; no interactive session capability supplied
```

**First approach and failure.** Calling successful authentication an unrestricted remote session ignored destination restrictions.

**Revised approach.** Separate key acceptance from command authority. Report the status-only capability and the missing prerequisite for the requested broader action.

**Independent controls.** The ordinary status action succeeds; an unrelated command never produces its requested marker. Preserve remote identity and key policy in the evidence.

**Completed result and limits.** Only the permitted status capability is supported. Broader movement, other keys, sockets and host authority remain untested.
