# Worked case: the filter lets data through but the sink remains parameterized

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Bound a supplied accepted-request observation.

```text
original string blocked by filter
alternate inert representation passes -> application 200
complete query path: decoded term bound as a value; returned rows=[]
benign search term -> expected owned row
no raw query/source concatenation supplied
```

**First approach and failure.** Calling the changed block status a successful SQL injection skipped the backend query boundary.

**Revised approach.** Trace the accepted value into the bound query and use the benign term as a reachability control. Filter acceptance is supported; SQL structure control is not.

**Independent controls.** Compare final query construction and result, not vendor or response status. Do not add payload families without a different supported parser hypothesis.

**Completed result and limits.** No underlying injection from this trace. Whether the filter itself violates an explicit contract is a separate policy question.
