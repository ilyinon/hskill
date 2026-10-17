# Worked case: the repository detector matches the SPA fallback

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Assess whether the supplied HTTP captures establish Git exposure.

```text
/.git/ -> 403
/.git/HEAD -> 200 text/html, <title>Portal</title>
/nonexistent-control -> same 200 body hash
no Git ref line, object bytes, or config section supplied
```

**First approach and failure.** Combining directory 403 and file 200 ignored the bytes and could trigger unnecessary full recovery.

**Revised approach.** Compare the identical fallback body and content structure. No Git artifact is established by these captures; retain the path as an unconfirmed lead only if more relevant evidence exists.

**Independent controls.** A real plain-text ref or detached object ID would be a different artifact, but still needs bounded follow-up. The nonexistent-path capture independently explains this response.

**Completed result and limits.** No repository exposure finding from this data. No repository content, secret validation, or reconstruction was performed.
