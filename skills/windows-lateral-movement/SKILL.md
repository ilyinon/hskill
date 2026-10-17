---
name: windows-lateral-movement
description: >-
  Windows lateral movement playbook. Use when pivoting between Windows hosts via PsExec, WMI, WinRM, DCOM, RDP, pass-the-hash, overpass-the-hash, or pass-the-ticket techniques.
---

# Windows Lateral Movement

## Working approach

- Record starting credentials/tickets, target rights, authentication protocol, reachable services, and protections
- Choose a compatible permitted remote-management method
- Verify the actual destination identity and action separately from transport/authentication success.

## Evidence and limits

The principal performs the documented authorized test action on the target under the claimed credential type.

SMB signing blocks relay conditions, not every valid credential-based SMB action; method prerequisites, UAC filtering, local policies, and file/service side effects matter.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. REMOTE EXECUTION METHODS COMPARISON; 2. PSEXEC VARIANTS; 3. WMI LATERAL MOVEMENT; 4. WINRM LATERAL MOVEMENT; 5. DCOM LATERAL MOVEMENT | [Read](./references/01-remote-execution-methods-comparison.md) |
| 6. PASS-THE-HASH (PTH); 7. OVERPASS-THE-HASH (PASS-THE-KEY); 8. PASS-THE-TICKET; 9. PIVOTING THROUGH COMPROMISED HOSTS; 10. LATERAL MOVEMENT DECISION TREE | [Read](./references/02-pass-the-hash-pth.md) |
| Advanced: Credential Dumping Techniques | [Read](./CREDENTIAL_DUMPING.md) |
