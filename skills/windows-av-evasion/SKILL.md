---
name: windows-av-evasion
description: >-
  AV/EDR evasion playbook for Windows. Use when bypassing AMSI, ETW, .NET assembly detection, shellcode execution, process injection, API hooking, and signature-based detection on Windows endpoints.
---

# Windows Av Evasion

## Working approach

- Identify the exact application/control, OS build, privileges, and observable blocked behavior in an authorized isolated environment
- Distinguish AMSI, ETW, user-mode hooks, kernel telemetry, and process protections
- Verify both the intended local action and remaining telemetry.

## Evidence and limits

A controlled reproduction establishes only the specified control's behavior and scope.

A per-process patch, clean scan result, or absent event is not proof of universal AV/EDR invisibility; detection-risk tables are not guarantees and live control tampering needs explicit scope.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. AMSI BYPASS OVERVIEW; 2. ETW BYPASS; 3. .NET ASSEMBLY LOADING; 4. SHELLCODE EXECUTION TECHNIQUES; 5. PROCESS INJECTION TECHNIQUES | [Read](./references/01-amsi-bypass-overview.md) |
| 6. UNHOOKING — BYPASS EDR API HOOKS; 7. PAYLOAD ENCRYPTION & OBFUSCATION; 8. SIGNATURE EVASION; 9. AV/EDR EVASION DECISION TREE | [Read](./references/02-unhooking-bypass-edr-api-hooks.md) |
| Advanced: AMSI Bypass Techniques — Detailed Patterns | [Read](./AMSI_BYPASS_TECHNIQUES.md) |
