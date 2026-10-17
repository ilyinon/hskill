# ai-ml-security: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Threat model and baseline | Specify supply-chain, model behavior, privacy inference or tool authority before selecting a metric. |
| Evaluation population | Record class balance, training/held-out split, query budget and independent control. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Membership classifier has high accuracy | Class imbalance or real membership signal | Compare majority baseline, TPR/FPR and held-out examples. |
| Model returns sensitive-looking text | Public/training artifact, hallucination or protected disclosure | Match a controlled independent marker and data-access provenance. |

## Interpret failure and finish the task

A model-loader error did not test an inference attack. A metric on the wrong population cannot establish privacy leakage or model extraction.

Track `precise hypothesis -> controlled data/model interface -> baseline-adjusted signal -> independent validation -> bounded impact`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
