# subdomain-takeover: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Complete DNS/resource chain | Attribute the name to the provider resource, region/tenant and current lifecycle. |
| Claimability evidence | Separate missing resource from provider ownership verification/reservation rules. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Provider error or NXDOMAIN | Stale mapping, temporary outage, or claimable resource | Check exact provider ownership requirements and non-mutating resource evidence. |
| Resource name is available | Name availability or domain binding permission | Determine whether serving the victim domain requires a separate ownership proof. |

## Interpret failure and finish the task

An unavailable DNS query is unknown state, not a takeover. A stale record can justify cleanup while claimability remains unverified; creating resources or binding domains is a separate scoped action.

Track `DNS record -> exact provider resource -> current claim prerequisites -> domain control or bounded uncertainty`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
