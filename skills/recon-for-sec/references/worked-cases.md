# Worked case: a narrow source audit can skip recon

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Choose the next workflow for an already supplied source boundary.

```text
task: audit supplied download handler; no live testing requested
source: authenticated member, global object-ID lookup, no ownership check
records: two owned test tenants
no unknown endpoint or service discovery question
```

**First approach and failure.** Opening broad port enumeration and directory catalogs would not reduce the uncertainty in this source audit.

**Revised approach.** Route directly to IDOR/BOLA and compare the same member against the two owned objects. Keep active discovery outside the requested task.

**Independent controls.** The owner records establish policy; absence of discovery is not a gap in this narrow deliverable, though other surfaces remain uncovered.

**Completed result and limits.** The routing decision and audit scope are complete. No broad assessment or external action has been performed.
