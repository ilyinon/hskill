# Worked case: an accepted update does not assign every supplied field

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Determine whether a profile update lets a regular user assign an administrator role.

```text
principal=member; stored={label: old, role: member}
complete update contract: bind only label; ignore other keys
input={label: new, role: admin}
response=200, stored={label: new, role: member}
admin-only action under same session=403
```

**First approach and failure.** Calling the successful PATCH mass assignment confused accepted request fields with committed protected fields.

**Revised approach.** Trace the binder allowlist and compare stored role and a role-dependent action. Only the permitted label changes.

**Independent controls.** A label-only update must succeed; the same session must retain member role and fail the admin action. Owner controls for nested objects remain a separate comparison.

**Completed result and limits.** No role escalation on this update path. Ignored unknown fields may be an API-design choice; other endpoints and child authorization are not covered.
