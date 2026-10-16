# attack-surface-mapping technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## Handoff

| Surface you drew | Load |
|---|---|
| Unauthenticated other-subject data, object ids | [auth-sec](../../auth-sec/SKILL.md), [idor-broken-object-authorization](../../idor-broken-object-authorization/SKILL.md) |
| Issue-session / reset / rebind / ticket-swap | [authbypass-authentication-flaws](../../authbypass-authentication-flaws/SKILL.md) |
| Differential filters, URL-fetch params, templates | [injection-checking](../../injection-checking/SKILL.md) |
| Upload / preview / convert | [upload-insecure-files](../../upload-insecure-files/SKILL.md) |
| Money / coupon / stock / approval | [business-logic-vuln](../../business-logic-vuln/SKILL.md) |
| REST / GraphQL / gateway docs | [api-sec](../../api-sec/SKILL.md) |
| Public middleware admin | [unauthorized-access-common-services](../../unauthorized-access-common-services/SKILL.md) |

## Anti-patterns

- Opening with directory brute or full-template scanning
- Grinding captcha / default passwords on login HTML
- Seeing a login page and changing assets
- Script extracted only paths; salts, ciphertext ids, hidden routes, demo accounts unread
- Treating 401 / 403 / login wall as dead
- Pouring a full matrix into the same login-code family
- Expanding to a new cluster while this application's live surface is unfinished
- Calling mapping "done" because the homepage returned 200
- Minting a new notes tree when the workspace or proxy project already holds the evidence
