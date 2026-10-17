# Worked case: a serialized-looking field reaches only a JSON data parser

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess a supplied source path without loading its data as executable objects.

```text
transport body=base64-encoded JSON
complete path: base64 decode -> JSON parser -> require string field label
result is a plain mapping; no class lookup or reconstruction hook
valid label -> stored literal label; malformed JSON -> parse error
```

**First approach and failure.** Choosing a runtime gadget generator from the transport encoding misidentified the reconstruction mechanism.

**Revised approach.** Trace the complete parser path. This entrypoint reconstructs data only under the supplied contract; inspect subsequent data consumers if a different boundary is suspected.

**Independent controls.** A benign valid label establishes the parser baseline; malformed input fails before use. Do not execute supplied serialized objects to classify their format.

**Completed result and limits.** No unsafe object-deserialization path is established here. This does not certify every loader, library or later use of parsed fields.
