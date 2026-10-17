---
name: csv-formula-injection
description: >-
  CSV/spreadsheet formula injection (DDE, Excel/LibreOffice, Google Sheets IMPORT*). Use when exports, imports, or user fields feed spreadsheets or reporting tools.
---

# CSV formula injection

## Working approach

Trace an untrusted field through export, actual import/reopen and final spreadsheet cell typing. Start with inert arithmetic and record product/version/locale.

## Evidence and limits

CSV quoting protects field structure, not cell typing. Distinguish literal text, formula evaluation, a warning and an external effect; verify any text-preserving mitigation after reopening.

## References

- For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md).
- For a complete change of approach and independent controls, read the [worked case](./references/worked-cases.md).
- For matching recipes, tools and detailed variants, read the relevant section of the [technical playbook](./references/legacy-playbook.md). Establish its actual parser, runtime or workflow prerequisites first.
