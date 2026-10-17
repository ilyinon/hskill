# Worked case: the preflight stops a non-simple state-changing request

Synthetic offline teaching case. The records below define the complete relevant
contract and observations; they are supplied evidence, not a claim that a real
product or exploit was executed. No target action is required to read this case.

**Goal.** Explain why a supplied cross-origin JSON attempt did not test a state-changing handler.

```text
action requires POST application/json plus X-Action header
browser trace: OPTIONS sent; origin not allowed; preflight fails
no POST in capture; owned setting stays old
valid same-origin action -> POST sent; setting becomes new
```

**First approach and failure.** Calling the missing CSRF field a proven action bypass ignored that the attempted action was never dispatched.

**Revised approach.** Classify this attempt as blocked before the handler. Inspect whether another accepted browser-sendable content type or route exists only if source/evidence supports it.

**Independent controls.** The same-origin action proves the operation works; capture absence of POST plus unchanged state distinguishes dispatch denial from an unreadable successful action.

**Completed result and limits.** No CSRF action is demonstrated by this attempt. Other request forms and endpoint policies remain unassessed; the teaching trace is not a browser execution test.
