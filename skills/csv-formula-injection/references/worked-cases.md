# Worked case: CSV quoting preserves syntax but the importer chooses formula type

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess harmless arithmetic in a supplied importer trace.

```text
untrusted value==1+1
CSV field bytes: "=1+1"
supplied importer trace: parsed field =1+1; cell type=formula; value=2
policy: exported untrusted field must remain literal text
text-typed control: cell value is literal =1+1, no formula
```

**First approach and failure.** Calling quoted CSV safe confused delimiter escaping with spreadsheet cell typing.

**Revised approach.** Trace the field into the importer. Enforce a text-preserving export/import contract and verify it survives reopen; CSV quoting alone is insufficient.

**Independent controls.** The same inert arithmetic must remain text after repair; ordinary strings and delimiter-containing fields must remain intact. Record the actual importer rather than claiming all products behave alike.

**Completed result and limits.** Formula interpretation violates this teaching text contract. No DDE, external request, command execution or real spreadsheet product was tested.
