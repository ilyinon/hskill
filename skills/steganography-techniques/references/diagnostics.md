# steganography-techniques: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual artifact/modality contract | Preserve source bytes and identify container, channel order, bit order and transformations. |
| Independent extracted structure | Use length, checksum or a separate format/parser rather than a promising string alone. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| strings finds no message | Bit-plane/compressed/encrypted data or genuinely absent content | Inspect format-supported channels with explicit parameters. |
| One extraction looks readable | Correct parameters or chance | Reproduce exact bytes and compare independent structure/check data. |

## Interpret failure and finish the task

A decoder error is not absence of hidden content. Do not alter the original; an entropy/signature guess needs independent validation.

Track `original bytes/channel -> exact extraction parameters -> recovered bytes -> independent format/check -> bounded interpretation`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
