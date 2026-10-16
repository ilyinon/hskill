# Test Matrix and Effort

Use with the shared scope/evidence rules in `SKILL.md` when broad assessment coverage is requested. What to hit first, what "tested" means per class, and when another permitted check can change the conclusion. Probe recipes live in deep topic skills.

## 1. Effort order

For observed in-scope surfaces, record tested evidence, not covered (reason), or N/A (an actual applicability reason). Time, missing access, or sufficient proof can end testing while applicable work remains not covered. Prioritize surfaces with plausible impact:

1. Unauthenticated access to another user, tenant, or subject
2. Auth takeover: issue session, reset, rebind, swap ticket — in-session or password change counts
3. Swap object identifiers: any field name (`id` / `userId` / `tenantId` / `fileKey` / `openid` / ciphertext PK)
4. Authenticated writes and business logic: add role, change amount or state, skip approval, coupon/inventory concurrency
5. Injection, SSRF, XSS, command or template execution on surfaces that show a **diff**
6. Salts, hardcoded keys, demo accounts in scripts and pages

No session: unauthenticated success → swap identifiers → auth endpoints → script keys → injection/SSRF/XSS/exec on differential surfaces.

With a session: swap identifiers while authenticated → add fields / skip steps / money → then put injection on business parameters that already return data.

Low-priority even if present: self-only CSRF, upload that only stores-and-downloads with no follow-on chain, login-form weak passwords.

Track observed GraphQL, upload, XML, WebSocket, and deserialization surfaces in coverage. Select checks relevant to the requested deliverable; record applicable untested work as not covered.

## 2. Type matrix

Classify applicable classes against the observed inventory. Distinguish a completed check, a confirmed finding, and untested work. Supported disclosure can be a finding; it does not establish unrelated impact.

| Class | Done means |
|---|---|
| Unauthenticated | Critical read/write with credentials stripped. On success, swap identifiers |
| IDOR | No account: after unauthenticated success, swap. With account: record same-subject baseline, then neighbor account, identifiers copied from responses, `0`/`-1`/empty, plus attachments/exports |
| Injection | Only endpoints where count, content, or a fetched URL can change. Each filter/sort/keyword param: baseline → probe → diff. A login gate leaves authenticated injection coverage untested unless source or scope establishes inapplicability. Pick probes for the actual stack; do not throw only quotes |
| SSRF | Inspect relevant URL/fetch inputs. Demonstrate an attributable destination-policy violation with a baseline/control; DNS-only events do not prove HTTP fetching. A complete source path can support a code finding |
| Command or template exec | Command, expression, template, deserialization, dangerous upload followed to execution or falsified |
| Credentials | Establish exposure; classify validity separately. Perform minimal read-only validation only when credential use, destination, and action are in scope; otherwise mark validity unverified |
| Default creds | Middleware/component naked defaults that actually issue a session. Login-form weak passwords are not mandatory. Hardcoded demo accounts are keys |
| Sensitive paths | Swagger / Actuator / debug / heapdump / env; secrets found here get mined |
| XSS | Reflected on reflection points; stored on write-then-read-back; combine with whether unauthenticated read is possible |
| Upload | Characterize validation, storage, retrieval, and access policy. Follow executable/SSRF/IDOR consumers only when supported and needed for the permitted deliverable |
| Path traversal | `file` / `path` / `filename` / `key` |
| CSRF | A browser-feasible cross-site action violates the session/action policy. Missing tokens alone are insufficient if another effective defense applies |
| Logic and privilege | Write endpoints that add role/amount/state; multi-step skip; money/coupon/stock to small or negative; claim/approval gets one concurrency pass. No such endpoint → N/A |
| Auth takeover | Inventory has issue-session, reset, rebind, ticket-swap, or step-up → tick. Login fields may reach an interpreter; determine applicability from the input flow |
| Other field surfaces | Classes this table does not name still get tested |

After classifying the surface, load the matching deep topic skill for probes (use `ROUTING.md` only when the topic is unclear).

## 3. When a partial chain warrants another check

Continue only if the next check can change the requested conclusion, remains authorized, and fits the budget. Sufficient proof or an action/stop limit ends the chain.

| You saw | Candidate next check when needed |
|---|---|
| File channel open | Business API, executable, path, or SSRF chain |
| OTP or slider passed | Does the code return in-band, bind an account, reset swap the user |
| Config has host but no creds | Keep looking for the full credential |
| Copied a secret | Establish exposure; validate only within authorization, or record validity unverified |
| Same-role readable, public static, HTTP 200 JSON | Compare owner/tenant policy; cross-owner private data may already prove BOLA, while a public object or status alone may prove nothing |
| Response sprouted id / download URL / token / internal host | Onto this site's queue |
| List or detail passed | Same object's attachment, export, preview, approval — one more shot |
| Medium already confirmed | Preserve the proved impact; follow another action only if the requested objective still needs it and scope permits |

## 4. Parameters, diffs, and response classes

Script inventory must answer whether these exist: business paths, signing salts, ciphertext identifiers, hidden routes, demo accounts. Write "none" only for inspected scope; uninspected material remains unknown.

Classify the response before spraying:

| Response looks like | It is | Do |
|---|---|---|
| One sentence "please log in", no list/total/roster/detail | Login gate | Record the auth gate and untested authenticated input; avoid blind probes |
| Has list / total / business fields, even `total=0` | Differential surface | Swap params, swap identifiers, inject per stack |
| Error, timeout, or length/timing clearly off baseline | Differential surface | Compare once or twice; stop if the diff is unstable |
| Missing a parameter dumps a roster or detail | Unauthenticated exception | Treat as unauthenticated + identifier swap |

1. Open the real page, capture the full request (query + body + headers).
2. List every filter and identifier field, including short enums.
3. On a differential surface, each filter param at least: normal, empty, illegal, stack-appropriate probe, and if needed a location change (query / json / header / path).
4. A diff is a lead: attribute changed count/content to the controlled input and confirm the violated policy, using the same-subject baseline and a negative control.
5. After a block, retry once with encoding or location change; still no diff → stop. Do not spray forever.
6. List passed → hit attachments and exports. Parent authorized, child often not.

## 5. Scope modes

**Locked** (user gave a fixed site or list):

- Do not scan unrelated brand lines before entering the site
- Record discovered gateways, API domains, and same-product hosts as candidates. Test only those included in the established scope; ownership or a link from the product is not additional authorization
- If the user marked priority assets, hit that group first; do not stall on the first login wall

**Exploratory** (user gave an org name and allowed boundary expansion):

- Multiple seeds become a queue; deep-mine one live cluster at a time
- Dedup, drop dead pages and non-alive hosts, then enter
- Remaining live surfaces on this cluster unfinished → do not fill progress with a new search
- Write a change log before the next cluster; re-request authorization if needed

A batch of sites that share the same login shell: finish auth endpoints on a representative, then on the others only look for new reset/rebind/ticket-swap paths. No new endpoint → do not open a full matrix per site.

## 6. Pre-conclusion self-check

- [ ] On differential surfaces, each filter param got an injection or IDOR diff
- [ ] Unauthenticated tested with credentials stripped
- [ ] Cross-user / cross-tenant tested — not only "tenant admin can read in-role"
- [ ] With a session: object graph, identifier swap, extra fields, step skip
- [ ] Upload followed to executable, SSRF, or business IDOR
- [ ] Auth chain followed past OTP / slider
- [ ] "Admin" was not misread as "in-role therefore not a bug"
- [ ] After a block, location or encoding changed; injection probes matched the stack
- [ ] This round did not over-index on unauthenticated reads
- [ ] Injection / SSRF / XSS / exec were actually tested, not one quote per path
- [ ] Confirmed medium on an object was chained up; response clues entered the queue
- [ ] Credential exposure and validity were recorded separately; validation stayed within scope
- [ ] Session findings were not written as anonymous unauthorized
- [ ] Portrait was written; scripts extracted more than paths
- [ ] Empty list / error was not treated as "please log in"
- [ ] List passed → attachments and exports were hit
- [ ] The full matrix was not poured into the same-family login code
