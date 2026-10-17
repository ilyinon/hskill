# classical-cipher-analysis: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Encoding and alphabet contract | Identify byte/text representation, allowed alphabet and any supplied known-plaintext constraints. |
| Independent candidate validation | Use re-encryption plus a check not derived solely from choosing readable text. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| A short candidate looks readable | Chance or one of several transforms | Check the complete message and independent structure/checksum. |
| Frequency ranking is weak | Too little text, non-language payload or wrong family | Use supplied format/known data instead of forcing a language guess. |

## Interpret failure and finish the task

A tool failure or invalid encoding does not disprove a cipher family. Printable output alone is not unique recovery; retain equivalent candidates until independent evidence resolves them.

Track `input representation/alphabet -> candidate transform -> full plaintext -> re-encoding and independent constraint`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
