# Worked case: the writable script is not the scheduled one

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied writable-task candidate without changing files.

```text
test-a can write /opt/tasks/report.sh
root task ExecStart=/usr/local/bin/report-safe; no symlink to writable script
complete supplied task inventory contains no consumer of /opt/tasks/report.sh
ordinary /opt/tasks/report.sh execution runs as test-a
```

**First approach and failure.** Calling the writable script root execution skipped which path the root task actually consumes.

**Revised approach.** Resolve ExecStart and its dependencies first. The controlled file has no supplied privileged consumer, so this candidate lacks the critical edge.

**Independent controls.** Compare exact canonical paths and execution users; a user-context run cannot validate a root effect. Keep unrelated privilege paths uncovered.

**Completed result and limits.** No privilege escalation through this candidate. Other tasks, interpreters, capabilities and runtime vulnerabilities were not assessed.
