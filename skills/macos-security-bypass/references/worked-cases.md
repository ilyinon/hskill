# Worked case: the displayed grant belongs to another process identity

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied privacy-permission trace.

```text
teaching privacy policy keys grants by responsible app identity
grant database: helper-A allowed test resource
actual responsible identity for request=app-B
resource attempt under app-B -> denied; no marker read
helper-A control -> allowed owned marker
```

**First approach and failure.** Calling the database row a grant to app-B ignored identity binding.

**Revised approach.** Compare the grant key with the actual responsible process. The supplied request is denied under the correct identity.

**Independent controls.** Use helper-A only as a distinct positive control, not as proof app-B crossed the boundary. Keep prompt and runtime state explicit.

**Completed result and limits.** No privacy-control bypass in this case. The teaching identity rule is supplied; no universal TCC/signing behavior or live OS test is claimed.
