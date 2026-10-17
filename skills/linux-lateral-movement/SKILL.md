---
name: linux-lateral-movement
description: >-
  Linux lateral movement playbook. Use after gaining initial access to pivot across Linux hosts via SSH hijacking, credential harvesting, internal pivoting, D-Bus exploitation, sudo token reuse, and shared filesystem abuse.
---

# Linux Lateral Movement

## Working approach

- Identify the current identity, credentials/agent sockets, trust configuration, reachable hosts, and permitted actions
- Distinguish credential access, forwarded authentication, IPC, and shared-filesystem paths
- Verify the destination identity with minimal authorized effect.

## Evidence and limits

A specific credential or trust relationship gives the starting principal a previously unavailable destination capability.

A key file, SSH_AUTH_SOCK, or reachable service is not confirmed access; key restrictions, agent availability, host policy, and ownership must agree.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SSH AGENT HIJACKING; 2. SSH KEY HARVESTING; 3. CREDENTIAL HARVESTING LOCATIONS; 4. D-BUS EXPLOITATION | [Read](./references/01-ssh-agent-hijacking.md) |
| 5. INTERNAL NETWORK PIVOTING; 6. SHARED FILESYSTEM EXPLOITATION; 7. SUDO TOKEN REUSE (ptrace-Based); 8. SYSTEMD SERVICE MANIPULATION; 9. LATERAL MOVEMENT DECISION TREE | [Read](./references/02-internal-network-pivoting.md) |
