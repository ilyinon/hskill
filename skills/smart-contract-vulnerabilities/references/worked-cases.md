# Worked case: the callback sees the balance already consumed

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied bounded withdrawal state-machine trace.

```text
owned caller credit=10; policy: total withdrawal <=credit
withdraw checks credit, sets credit=0, then external transfer10
callback attempts withdraw again -> sees0, denied
final total transferred=10, stored credit=0
teaching trace assumes the outer transfer commits successfully
```

**First approach and failure.** Calling any callback a repeat-withdrawal exploit ignored the state visible at reentry and final total.

**Revised approach.** Trace checks/effects before the external call and sum committed transfers. The nested attempt is denied after the entitlement is consumed.

**Independent controls.** A normal non-reentrant withdrawal must transfer10 and leave0; a second later call also denies. Failed-transfer rollback needs its own supplied contract.

**Completed result and limits.** No excess withdrawal in this trace. No full Solidity/EVM implementation, compiler behavior, other callback route or proxy layout is validated.
