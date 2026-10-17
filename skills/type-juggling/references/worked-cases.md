# Worked case: the strict string comparison rejects the numeric-looking token

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Interpret a supplied token-comparison contract.

```text
stored token is string "0e12"; candidate is distinct string "0e99"
complete verifier requires a string and uses strict string equality
candidate -> reject; stored token -> accept
non-string array -> reject before comparison
no loose == or numeric cast on this path
```

**First approach and failure.** Applying the magic-numeric-string recipe assumed a loose operator absent from the source.

**Revised approach.** Trace the strict comparison and type guard. Distinct numeric-looking strings remain different text in the supplied verifier.

**Independent controls.** Keep both operands and operator explicit; the exact stored token is the positive control and a non-string input is a separate pre-comparison rejection.

**Completed result and limits.** No coercion-based token bypass on this path. Other runtime expressions, casts, hash APIs and error handlers remain unassessed.
