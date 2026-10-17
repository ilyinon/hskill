# Worked case: the writable sibling is outside the actual service path

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied service-path candidate.

```text
service binary is quoted exact path C:\Program Files\Vendor\safe.exe
test-a can write C:\Program Files\Vendor-Old only
actual safe.exe and its dependency directories are not writable by test-a
no other lookup or configuration path supplied
```

**First approach and failure.** Inferring service hijack from a similarly named writable directory ignored the exact consumer path and ACL.

**Revised approach.** Resolve the quoted binary and its supplied dependency paths. The writable sibling does not provide control of the service input in this model.

**Independent controls.** Compare canonical paths and effective write rights, not a directory-name substring. Service-account metadata alone is not a new capability.

**Completed result and limits.** No escalation through this candidate. Other service settings, tasks, tokens and unprovided dependencies remain unassessed.
