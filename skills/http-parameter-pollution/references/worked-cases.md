# Worked case: the validator selects the first value and the handler uses the last

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Audit the supplied duplicate-key contract.

```text
raw pairs: item=owned-a&item=owned-b
session A may act only on owned-a; owned-b belongs to test tenant B
validator selects first -> allows owned-a
handler selects last -> returns B marker
normal single owned-a -> A marker
```

**First approach and failure.** Looking only at the validator result obscured that a different value reached the handler.

**Revised approach.** Compare selected values at both layers. Parse once and share the canonical result, or reject ambiguous duplicates before the policy decision.

**Independent controls.** Own single value remains allowed; foreign single value denies; duplicate mixed values deny or resolve consistently before authorization.

**Completed result and limits.** A validation/use mismatch supports the supplied private-read flaw. No assumptions about all frameworks or every content type follow.
