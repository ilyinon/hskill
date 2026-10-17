# Worked case: a foreign object ID is not path traversal

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Select a focused review from a file-download source path.

```text
GET /files/{id}; fixed member=A
lookup is files[id]; disk paths are generated constants under /srv/files
id=b7 returns B-private marker; no owner filter
input never becomes a filesystem path
```

**First approach and failure.** Using ../ payload families would test a path interpretation that the supplied code does not have.

**Revised approach.** Route to IDOR/BOLA for the missing owner relation. Preserve the independent fact that filesystem path selection is not caller-controlled in this handler.

**Independent controls.** Own ID succeeds, foreign owned-test ID should deny under the same session, and nonexistent ID is a separate lookup control.

**Completed result and limits.** A source-supported private-file read finding, with no traversal or execution claim. Other upload stages require their own evidence.
