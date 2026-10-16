---
name: cmdi-command-injection
description: >-
  Command injection playbook. Use when user input may reach shell commands, process execution, converters, import pipelines, or blind out-of-band command sinks.
---

# Cmdi Command Injection

## Working approach

- Trace the input into the actual shell, executable, argument list, or environment
- Identify quoting, platform, decoding, and whether a shell is invoked
- Use a harmless controlled effect and an independent baseline before selecting a syntax family.

## Evidence and limits

An input-controlled interpreter or argument boundary causes the specific permitted execution effect.

A metacharacter, 500 response, or isolated delay does not prove command execution; shell injection and option/argument injection have different prerequisites.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SHELL METACHARACTERS (INJECTION OPERATORS); 2. COMMON VULNERABLE CODE PATTERNS; 3. BLIND COMMAND INJECTION — DETECTION; 4. INJECTION CONTEXT VARIATIONS | [Read](./references/01-shell-metacharacters-injection-operators.md) |
| 5. PAYLOAD LIBRARY; 6. FILTER BYPASS TECHNIQUES; 7. COMMON INJECTION ENTRY POINTS; 8. BLIND INJECTION DECISION TREE; 9. ADVANCED WAF BYPASS TECHNIQUES | [Read](./references/02-payload-library.md) |
| 10. PHP disable_functions BYPASS PATHS; 11. COMPONENT-LEVEL COMMAND INJECTION; 12. WINDOWS CMD.EXE VS POWERSHELL INJECTION MATRIX | [Read](./references/03-php-disable-functions-bypass-paths.md) |
| 13. CONTAINER / K8S EXEC INJECTION; 14. ENVIRONMENT VARIABLE INJECTION | [Read](./references/04-container-k8s-exec-injection.md) |
