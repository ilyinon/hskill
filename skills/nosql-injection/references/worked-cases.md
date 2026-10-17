# Worked case: type validation rejects the object before query construction

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a complete string-only lookup contract.

```text
endpoint accepts username as string; other types return 400 before query
input username={operator: any} -> 400, query count=0
input username=test-a -> query equality(username, test-a), own row
input username=missing -> no row
no raw query object is passed from caller
```

**First approach and failure.** Calling the 400 an operator-execution response skipped the upstream type guard.

**Revised approach.** Trace the string check and equality construction. The supplied object never becomes query syntax.

**Independent controls.** A benign present and absent username establish real query reachability; object rejection must preserve query count zero. Inspect other filter APIs only if supplied.

**Completed result and limits.** No structure-injection flaw in this entrypoint. No claim about a particular database server or all NoSQL paths is made.
