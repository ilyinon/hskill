For other original section numbers, use the [entry index](../SKILL.md#references).


# Attack Surface Mapping

Given **one target** and **one application**, draw the surface from what that application already exposes. Then stop. Testing lives in other skills.

This skill is the fast path. Success is a portrait plus a host/API inventory plus a key table plus response-class labels plus an object graph. A probe count is not success.

Field patterns for where the rest of the surface actually lives: [SURFACE_PATTERNS.md](../SURFACE_PATTERNS.md).

## When

- A new URL, a new app, or "I only see a login page"
- Need to know **what** to test before loading injection / auth / upload skills
- The agent is about to brute directories, spray quotes, or expand to unrelated hosts

Do **not** use this skill to expand an organization-wide host universe. Map the current application cluster. Finish it. Then, if scope allows, take the next cluster.

Authorization and destruction bounds: [hack](../../hack/SKILL.md) start gate. Stay in scope.

## What must exist (not a file tree)

Before any vulnerability skill, these facts must be retrievable. Persist them in whatever the local workspace already uses for notes and evidence — an existing task folder, a proxy project, session notes, a ticket. Do not invent a new directory layout when one is already in play.

| Fact | Keep |
|---|---|
| Portrait | 3–5 sentences, not an essay |
| Hosts | Business hosts, gateways, API domains this app already named |
| Endpoints | Method, path, params, auth required? |
| Keys | Signing salt, ciphertext id + frontend pubkey, hidden/admin route, hardcoded demo account. Record `none` per row if absent |
| Response class | Login-gate / differential / unauthenticated exception |
| Object graph | list → detail → attachment / export / approval |

Requests, diffs, and screenshots stay where they were captured when that store is already the working set. Empty inventory plus "I will brute paths next" is a failed mapping.

