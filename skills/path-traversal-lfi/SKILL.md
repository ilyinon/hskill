---
name: path-traversal-lfi
description: >-
  Path traversal and LFI playbook. Use when file paths, download endpoints, include operations, archive extraction, or wrapper behavior may expose filesystem control.
---

# Path Traversal Lfi

## Working approach

- Trace the input through decoding, path joining, canonicalization, root constraints, and the final read/include operation
- Identify OS and runtime semantics
- Use an owned marker file outside the intended root before selecting wrappers or include chains.

## Evidence and limits

The application reads or includes a controlled file across the intended filesystem boundary.

An error path, existence oracle, or encoded traversal string is not file disclosure or execution; distinguish traversal, LFI, RFI, and handler-specific processing.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE CONCEPT; 2. TRAVERSAL SEQUENCE VARIANTS; 3. TARGET FILES AND ESCALATION TARGETS; 4. PHP LFI → RCE TECHNIQUES | [Read](./references/01-core-concept.md) |
| 5. PHP FILTER WRAPPER (FILE CONTENT READ); 6. REMOTE FILE INCLUSION (RFI) — WHEN ENABLED; 7. SERVER-SPECIFIC PATH TRUNCATION; 8. PARAMETER LOCATIONS TO TEST; 9. FILTER BYPASS CHECKLIST; 10. IMPACT ESCALATION PATH; 11. LFI TO RCE ESCALATION PATHS; 12. PHP WRAPPER EXPLOITATION MATRIX; 13. PEARCMD LFI EXPLOITATION; 14. WINDOWS-SPECIFIC LFI TECHNIQUES | [Read](./references/02-php-filter-wrapper-file-content-read.md) |
| 15. PARAMETER NAMING PATTERNS (HIGH-FREQUENCY TARGETS); 16. LFI TO RCE — ESCALATION PATHS; 17. PHP WRAPPER EXPLOITATION MATRIX; 18. PEARCMD LFI TO RCE | [Read](./references/03-parameter-naming-patterns-high-frequency-targets.md) |
| 19. PARAMETER NAMING PATTERNS & HIGH-FREQUENCY ENDPOINTS; 20. JAVA / SPRING PATH TRAVERSAL; 21. TOMCAT-SPECIFIC TRICKS; 22. NGINX ALIAS MISCONFIGURATION; 23. NODE.JS PATH MODULE QUIRKS; 24. IIS SHORT FILENAME ENUMERATION (~1 TILDE TRICK) | [Read](./references/04-parameter-naming-patterns-high-frequency-endpoints.md) |
