# Symmetric/PRNG tasks: establish the construction and validate the recovered state

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Mode, primitive, and integrity layer | Inspect format/source and authenticated error stages; length alone does not identify the construction. |
| Exact bytes and layout | Separate IV/nonce, ciphertext, tag, encoding, and known plaintext; preserve byte indexes and endianness. |
| Oracle or observation provenance | Check whether output is full, consecutive, from one generator, or truncated/filtered/skipped. |
| Requested result | Distinguish plaintext recovery, integrity change, state recovery, next-output prediction, and original-seed recovery. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Modified ciphertext is rejected | Authentication/tag gate, parser error, or padding behavior | Locate the rejection stage. A uniform tag rejection is not a padding oracle. |
| A padding candidate works once | Actual valid padding or accidental original padding | Use an independent byte perturbation/control before extending the recovered block. |
| Untempered MT words reproduce old outputs but miss the future | Wrong state index, order, gaps, or wrong generator | Check the observation contract and state installation/index separately from inverse arithmetic. |
| Repeated ciphertext block | ECB candidate, repeated records, or chosen format | Verify alignment and construction before applying a cut-and-paste recipe. |
| A script raises on length/type | Decode/layout or tool setup failure | Restore the exact byte representation; no cryptanalytic hypothesis has been tested yet. |

## Close the requested task

Track `observations → construction assumptions → recovered intermediate → installed state/plaintext → independent withheld check`. A recovered word list is not a prediction, and a prediction is not a seed. For a bounded lab, verify future outputs or a plaintext invariant before declaring completion. If an integrity gate removes the required oracle, change the hypothesis rather than varying the same unauthenticated modification. Never generalize a CPython MT result to a cryptographic RNG.
