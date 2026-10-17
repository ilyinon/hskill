---
name: memory-forensics-volatility
description: >-
  Memory forensics playbook using Volatility 2/3. Use when analyzing memory dumps for malware analysis, credential extraction, process investigation, code injection detection, and incident response timeline reconstruction.
---

# Memory Forensics Volatility

## Working approach

- Preserve image provenance, hash, acquisition context, and time basis
- Identify OS/symbol compatibility before selecting plugins
- Correlate process, connection, module, and persistence artifacts across independent views.

## Evidence and limits

A reproducible timeline and corroborated artifacts support the stated behavior and its uncertainty.

A process name, RWX region, plugin hit, or missing process alone does not prove malware; acquisition gaps, paging, symbols, and benign software cause false positives.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. MEMORY ACQUISITION; 2. VOLATILITY 2 vs 3; 3. ANALYSIS METHODOLOGY | [Read](./references/01-memory-acquisition.md) |
| 4. LINUX MEMORY ANALYSIS; 5. MALWARE INDICATORS IN MEMORY; 6. DECISION TREE | [Read](./references/02-linux-memory-analysis.md) |
| Advanced: VOLATILITY CHEATSHEET — Vol2 / Vol3 Command Reference | [Read](./VOLATILITY_CHEATSHEET.md) |
