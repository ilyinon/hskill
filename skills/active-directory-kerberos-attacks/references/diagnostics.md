# active-directory-kerberos-attacks: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Ticket and intended service | Record client/server principals, realm, ticket type, validity, key version and target SPN. |
| Accepted identity and authorization | Separate obtaining/importing a ticket from service acceptance and action permission. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Ticket file exists or imports | Cache possession, not necessarily target acceptance | Inspect the ticket service principal and service response. |
| Authentication succeeds but action denies | Valid service identity without the required privilege | Compare resulting identity and exact authorization policy. |

## Interpret failure and finish the task

A clock, cache-format or SPN error can break setup without testing the proposed privilege path. A captured hash/ticket is not plaintext recovery or domain control.

Track `credential/key prerequisite -> correct ticket -> intended service acceptance -> mapped identity -> permitted action`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
