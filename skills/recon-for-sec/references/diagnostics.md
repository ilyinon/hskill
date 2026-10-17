# recon-for-sec: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Target type and existing evidence | Determine whether this is one app, a supplied artifact, or a broad asset assessment. |
| Scope and handoff | Preserve exact hosts/actions and choose one observed boundary. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Only a target URL is given | Unknown app surface | Start with application mapping, not every specialist. |
| A source file already shows an object-policy question | Known narrow audit | Route directly to the specialist rather than repeating full recon. |

## Interpret failure and finish the task

A discovery tool problem is a setup/coverage issue. Known narrow questions do not need all earlier recon stages.

Track `user task -> authorized evidence -> minimal surface mapping or direct topic -> bounded handoff`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

Known object questions can use [IDOR](../../idor-broken-object-authorization/SKILL.md) directly; unknown apps use [surface mapping](../../attack-surface-mapping/SKILL.md).
