# IDOR: prove the subject-object relationship at the actual handler

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Subject and authentication state | Keep the session fixed; record user, tenant, scopes, and effective role. |
| Object policy and ownership | Use owned test objects and their authorized representation; public sharing changes the expected result. |
| Child/reference relationships | Identify whether a preview, attachment, export, or nested route is bound to the authorized parent. |
| Enforcement location | Trace middleware, service, and query filters before treating an absent inline check as missing authorization. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Foreign parent returns 403 | Effective parent control; child paths may enforce differently | Inspect the child handler/query rather than assuming shared enforcement. |
| Child returns 200 | Own/public object, login shell, or an unbound foreign reference | Compare owner/tenant, body, sharing policy, and a valid owner baseline. |
| Changed session accesses admin data | Different principal with legitimate privilege | Return to a fixed low-privilege session; this is not an escalation control. |
| Opaque identifier is hard to guess | Identifier discovery constraint | Use a reference supplied by the second owned account; do not equate opacity with authorization. |
| Object is loaded before a check | Internal loading may be safe | Trace what is actually returned or changed after the check; loading alone is not disclosure. |

A valid denied object disproves that request path, not every action or child. A lookup failure or unavailable second account leaves the corresponding comparison incomplete.

## Close the requested task

Track `fixed subject → authorized parent → selected child → returned/changed protected state`. Find which edge loses the relationship. For a finding, preserve ownership and allowed/breaking/owner controls. For a fix, constrain the actual selected object and its parent relationship before response or mutation. Avoid inferring write, bulk, or production impact from one read.
