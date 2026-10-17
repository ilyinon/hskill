# Worked case: upload succeeds but the actual flaw is preview authorization

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Follow an uploaded inert marker to the boundary that fails.

```text
A uploads inert text marker A-PRIVATE; stored opaque ID=f17
file download enforces owner; B download f17 -> 403
preview handler loads f17 globally without owner/share check
same B session + preview f17 -> 200, A-PRIVATE
storage never executes text
```

**First approach and failure.** Pursuing script extensions after upload success missed the demonstrated ownership failure at preview.

**Revised approach.** Trace the same opaque ID through both retrieval paths and add equivalent owner/share enforcement before preview returns content.

**Independent controls.** A must still preview its own file; B must deny on both routes; a deliberately shared test file follows its separate policy.

**Completed result and limits.** A supplied private-preview read flaw is supported. No execution, parser exploit or filesystem overwrite is established.
