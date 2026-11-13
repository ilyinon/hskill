# active-directory-certificate-services: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Enrollment and issuance prerequisites | Record current template/CA policy, effective enrollment right, approval and certificate purpose. |
| Mapping and authentication | Separate an issued certificate from trusted identity mapping and usable service authority. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Template permits requester-supplied naming | Candidate path or blocked enrollment/approval/mapping | Inspect every gate on the same CA/template and build. |
| Certificate is issued | It may map to the requester or no accepted account | Correlate actual mapping identity and authentication outcome. |

## Interpret failure and finish the task

A failed request before issuance does not test certificate mapping. Issuance alone does not demonstrate impersonation; historical ESC labels are candidates until current conditions agree.

Track `enrollment right -> issuance requirements -> certificate -> trusted identity mapping -> accepted capability`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review CA and template policy together

Inventory which templates each CA publishes and who can enroll or modify them. Review requester-controlled subject fields, approval requirements, and intended usages alongside certificate mapping policy. Verify approved enrollment and denial from an unapproved group using configuration records or a controlled policy check. [Microsoft AD CS guidance](https://learn.microsoft.com/windows-server/identity/ad-cs/secure-delegate-audit-certification-authority)
