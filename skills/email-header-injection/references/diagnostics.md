# email-header-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Message header versus SMTP envelope | Trace user fields through library serialization and recipient selection. |
| Actual transport bytes | Use supplied raw message and envelope logs with inert owned mailbox markers. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Cc/Bcc text appears in Subject | Single encoded field or parsed extra header | Inspect raw field boundaries and parsed header list. |
| Bcc absent from stored message | Normal removal or no extra delivery | Check envelope recipients rather than message display alone. |

## Interpret failure and finish the task

A mail API rejection is not delivery. SPF/DKIM/DMARC verdicts concern distinct authentication/alignment properties and do not alone establish header injection.

Track `user field -> serializer -> parsed headers and envelope recipients -> accepted delivery -> scoped impact`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
