# Worked case: template-looking data is never recompiled

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess the supplied rendering source without running an engine payload.

```text
fixed template source: <p>{{ label }}</p>
label value={{7*7}}
complete contract: compile fixed source once; substitute/escape label as data; no recursive compilation
result text={{7*7}}; known template arithmetic baseline evaluates in source
```

**First approach and failure.** Testing more expression syntaxes inside the same data slot cannot create a compilation step absent from the source.

**Revised approach.** Trace source compilation and data substitution separately. The supplied value remains data, so this path does not evaluate caller template source.

**Independent controls.** A plain label and the expression-like label survive as text; the source-only arithmetic baseline verifies that the engine itself works without confusing input position.

**Completed result and limits.** No SSTI on this path. Other template-source features, client rendering and runtime capabilities remain unassessed.
