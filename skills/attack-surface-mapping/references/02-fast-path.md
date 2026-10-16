# attack-surface-mapping technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## Fast path

```
Portrait
  → find the business plane (login is a shell)
  → inventory from the app (JS / traffic / docs), keys not just paths
  → classify responses
  → grow the object graph from responses
  → same-skin / same-gate collapse
  → surface-done → hand off
```

Do not insert directory brute, full-template scanning, or password spraying into this loop.

### 1. Portrait (mandatory, before any request spray)

Three to five sentences:

- Who uses this (consumer / merchant / operator)
- Core objects (order, ticket, coupon, document, tenant)
- Which fields hold money, privilege, or state
- What an unauthenticated caller can already touch

Cannot write it → capture one real page's traffic first. Do not scan into a blank portrait.

Mini-program, native app, GraphQL, WebSocket, batch export, agent-with-tools, template preview, file convert, command RPC: treat as **this site's surface**, not a sidenote.

### 2. Find the business plane

A login page is a shell. The surface is the post-login business host or the **same-host gateway behind the form**. Seeing a login page is not a reason to change assets.

Find the plane without logging in:

- Query: `service=` / `redirect_uri=` / `callback=` / `returnUrl=` / `jumpUrl=` / `next=`
- Client: `env.js` / `baseURL` / `apiHost` / `/prod-api` / `VUE_APP_*` / `REACT_APP_*`
- Transport: 302 `Location`, `X-Frame-Options: ALLOW-FROM`
- Naming: same-product `api` / `admin` / `gateway` / product host

Someone else's SSO / CAS / OAuth page: do not audit the identity product. Follow it back to **this** product's business plane. Criterion: the login page's owner is not this business.

Alive vs dead:

| Treat as alive | Treat as dead |
|---|---|
| 401, 403, login wall, admin challenge | Timeout, parking page, no business response |
| Management console challenge | Default CDN / empty static shell with no script |

Alive ≠ grind the form. Captcha OCR, slider farms, and login-box dictionaries are not mapping.

Form checks that are in-scope for mapping (once, then stop): empty password, skip-password step, extra fields on the login API (`tenant` / `corpId` / `moduleId`), business paths already visible next to the form (list / detail / stats). Username and password boxes are not business parameters.

### 3. Inventory from the application

**Frontend present:** open a business page → collect scripts (including async chunks and sourcemaps) → extract APIs **and keys** → capture traffic to fill gaps → persist endpoints and keys in the local evidence store.

JS extracts more than `/api/` paths. For each row, write the value or `none`:

| Extract | Why it is surface |
|---|---|
| `/api/` paths, RPC cmd numbers, GraphQL operations | Endpoint list |
| Signing salt, hardcoded key, `sign` that does not need a cookie | Replay without a session |
| Ciphertext id + frontend public key (`modulus` / JSEncrypt) | Neighbor-id is encryptable |
| Hidden / admin routes in the router, unpublished chunks | APIs the UI never shows |
| Hardcoded demo account, test tenant, experience entry | A key, not a login-form dictionary |
| Command / template / expression / file-convert / RPC-with-exec / agent tools | Execution plane; do not invent params if none exist |

**No frontend / JS blocked:** Swagger, OpenAPI, captured traffic, HTML inline, known gateway prefixes. Do not idle waiting for a full JS dump.

**Frontend present but inventory empty → directory brute** is forbidden.

Docs and debug planes, if this app already linked them: [api-recon-and-docs](../../api-recon-and-docs/SKILL.md). Exposed VCS / backups: [insecure-source-code-management](../../insecure-source-code-management/SKILL.md). Both are *this cluster's* extra planes, not a new search.

### 4. Classify responses before any probe

| Response | Class | Mapping action |
|---|---|---|
| One sentence "please log in" / `NotLogin`, no list / total / roster / detail | Login gate | Do not mark as an injection surface |
| Has list / total / business fields, even `total=0` | Differential | Keep on the test list |
| Error, 500, timeout, or length/timing off baseline | Differential | Keep; unstable diff → stop after one or two compares |
| Missing a parameter dumps a roster or detail | Unauthenticated exception | Highest-priority unauth surface |

An empty list is "structure returned, count is 0", not a login gate.

### 5. Object graph is surface

Identifiers in any field name (`id` / `userId` / `tenantId` / `fileKey` / `openid` / ciphertext PK) are surface.

Walk, and write it down:

```
list → detail → attachment / export / preview / approval
```

Parent authorized, child often not. After a list passes, the next surface is the attachment, not a new host.

Anything a response newly names — id, download URL, token, internal host, role field — goes onto **this site's** queue immediately. Do not drop it when changing pages.

### 6. Collapse same-skin and same-gate

Fingerprint-same (title, skeleton, build hash, API prefix, login chain): pick 2–3 representatives. Siblings only get a glance: new path / new port / another app / another `jump` / `service=` / `moduleId` business plane. No new plane → do not open a full matrix.

**Same-gate** (all four):

1. Business paths already extracted
2. Unauthenticated exceptions already probed
3. Remaining business endpoints return the **same login-code family**
4. No unauthenticated other-subject data, and no missing-param dump

Then stop this gate. Siblings with the same `baseURL` + same code: glance for new paths or a code change. Auth endpoints (issue session / reset / rebind / ticket-swap) still go on the list if present; they are not "please log in, so skip".

Same host is not same-skin. Extra paths on the same host always expand.

No business script, default server page, or leftover behind the same login-code family: falsify once and leave. Do not pad with a full matrix.

### 7. Surface-done (then hand off)

Mapping is done when:

1. Portrait exists, or this is recorded as a shell with no business object
2. Endpoint inventory exists (full or degraded); keys have values or `none` — in the local evidence store, not a prescribed path
3. Response classes labeled; unauthenticated exceptions ticked
4. Object graph recorded, or recorded as unlistable
5. Same-skin / same-gate leftovers glanced, not rematrixed
6. Auth endpoints listed if the inventory has issue-session / reset / rebind / ticket-swap / 2FA — listed, not yet exploited

Then load [hack](../../hack/SKILL.md) for effort order and the matching category skill. Do not start testing inside this file.

