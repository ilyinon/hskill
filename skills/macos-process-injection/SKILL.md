---
name: macos-process-injection
description: >-
  macOS process injection playbook. Use when you need to inject code into running or launching macOS processes via dylib hijacking, DYLD environment variables, XPC exploitation, Mach port manipulation, or Electron/Chromium abuse.
---

# Macos Process Injection

## Working approach

- Record macOS/build, architecture, signing, Hardened Runtime, entitlements, SIP, and target identity
- Distinguish loader/search-path, XPC/Mach, scripting, and process-memory boundaries
- Verify a reachable path under the real launch context.

## Evidence and limits

A controlled local test crosses the specified process or service trust boundary under documented prerequisites.

DYLD variables or a missing dylib alone do not imply injection; signing, library validation, protected processes, entitlements, and launch environment matter.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. DYLD_INSERT_LIBRARIES INJECTION; 2. DYLIB HIJACKING; 3. XPC EXPLOITATION | [Read](./references/01-dyld-insert-libraries-injection.md) |
| 4. MACH PORT MANIPULATION; 5. MIG (MACH INTERFACE GENERATOR) ABUSE; 6. ELECTRON / CHROMIUM INJECTION; 7. APPLICATION SCRIPTING (APPLE EVENTS); 8. PROCESS INJECTION DECISION TREE; 9. DETECTION & FORENSICS | [Read](./references/02-mach-port-manipulation.md) |
| Advanced: Dylib Hijacking & XPC Exploitation — Step-by-Step Techniques | [Read](./DYLIB_XPC_TECHNIQUES.md) |
