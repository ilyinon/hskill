# lattice-crypto-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Original algebra and bounds | Record modulus, polynomial/linear equations, unknown range and independent sample facts. |
| Lattice model fidelity | Check scaling, dimensions, embedding and why a short vector should encode the unknown. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| LLL returns a short vector | Reduction completed, not necessarily the desired secret | Substitute the decoded candidate into the original equations and bounds. |
| Candidate fits some samples | Overfit, wrong scaling or ambiguous solution | Use withheld/original constraints and report remaining alternatives. |

## Interpret failure and finish the task

A Sage/solver error is setup failure. A mathematically valid residue outside the declared small-root range is not the requested bounded solution.

Track `original equations/bounds -> faithful lattice/model -> decoded candidate -> original constraints -> independent validation`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
