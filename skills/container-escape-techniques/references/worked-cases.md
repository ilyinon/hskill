# Worked case: namespace root is mapped to an unprivileged host identity

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret the supplied identity and access trace.

```text
inside UID=0
supplied user map: inside 0 -> host 100000
host-root resource /host-root-marker denies host UID 100000
mount available inside is a read-only owned fixture
no privileged host API/socket or writable host mount supplied
```

**First approach and failure.** Calling UID 0 a host escape ignored the user namespace and the denied host-side operation.

**Revised approach.** Trace the UID mapping and actual resource decision. The supplied identity does not have host-root authority.

**Independent controls.** An ordinary in-container owned file remains readable. The host marker denial is a resource control, not merely a cosmetic namespace label.

**Completed result and limits.** No host boundary crossing in this case. Other runtime vulnerabilities, mounts and capabilities remain separate hypotheses; no container or host was modified.
