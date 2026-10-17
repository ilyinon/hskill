# Worked case: the failure is a read-only mount, not seccomp

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Diagnose a supplied operation failure before selecting a bypass family.

```text
same user reads /fixture/item -> success
write attempt returns EROFS; supplied mount record marks /fixture read-only
supplied syscall policy permits the write syscall; no seccomp denial record
separate writable owned path accepts ordinary write
```

**First approach and failure.** Opening syscall-filter escape recipes misidentified the gate indicated by the error and mount context.

**Revised approach.** Attribute the denial to the read-only mount. Use the already permitted writable path if it satisfies the user task; changing mount authority is a separate unavailable prerequisite.

**Independent controls.** The read baseline and writable-path control isolate filesystem policy from an unusable tool. No mount or security policy is altered in this teaching analysis.

**Completed result and limits.** The failed edge is diagnosed; no read-only or syscall boundary has been bypassed. Access at another path is not unrestricted filesystem authority.
