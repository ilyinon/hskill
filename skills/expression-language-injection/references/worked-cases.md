# Worked case: evaluation is confined to a deliberately limited arithmetic grammar

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Explain the capability demonstrated by a supplied evaluator trace.

```text
teaching service intentionally accepts arithmetic expressions
allowed grammar: integer literals, +, *, parentheses
2*(3+4) -> 14
method/type lookup token -> grammar rejection before evaluation
policy: arithmetic is allowed; runtime object access is forbidden
```

**First approach and failure.** Calling arithmetic output full runtime execution ignored the service policy and evaluator grammar.

**Revised approach.** Identify the permitted language and rejection stage. Arithmetic works as designed; the supplied runtime-access candidate is rejected before evaluation.

**Independent controls.** A plain integer and arithmetic expression establish valid behavior; an unsupported token and malformed expression establish different rejection paths.

**Completed result and limits.** No runtime-access policy violation is shown. The result does not establish safety of every EL implementation, integration or extension context.
