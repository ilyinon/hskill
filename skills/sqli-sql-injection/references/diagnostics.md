# SQLi: identify the query component under control

Read when choosing a technique, interpreting a failed attempt, or deciding the next useful check. Use only rows matching the observed task; this is not an extra mandatory sweep.

## Establish applicability and branch on evidence

| Required fact | Smallest useful check |
|---|---|
| Database, driver, and query-building path | Read the actual execute call and binding arguments; choose syntax for the observed engine. |
| Input position | Separate bound value, identifier, ordering expression, clause, and second-order stored value. |
| Expected operation and result | Establish normal rows, ordering, errors, and applicable access policy before interpreting a difference. |
| Stable execution | Separate application/driver exceptions, WAF rejection, query execution, and cache hits. |

| Observation | Competing explanations | Discriminating check and next step |
|---|---|---|
| Quotes in search return no extra rows | Proper value binding, ignored parameter, or an unexercised branch | Inspect the value binding and test a benign term that changes results. Then inspect other query components independently. |
| Invalid sort produces a DB error | A raw ordering expression, an invalid allowed value, or a wrapper error | Trace how sort reaches SQL; compare a documented sort with an unapproved but valid engine expression. |
| A boolean/time probe has no effect | Wrong context, unsupported syntax, upstream denial, or a true negative | Confirm the normal branch executes, then use a context-specific control. A failed dialect guess is not class-wide disproof. |
| One slow response | Queueing, locks, network retries, or query work | Establish repeatable matched controls or inspect the query path; do not call one delay an oracle. |
| Driver refuses multiple statements | One-statement API restriction | Analyze the reachable single statement; this error does not establish parameterization. |

Treat structure control and business impact separately. Authorized ordering changes are ordinary features; an input that selects raw SQL outside a finite sort policy demonstrates a different boundary.

## Close the requested task

Map `input component → constructed statement/binding → observed semantic change → policy impact`. A source audit can finish at a complete unsafe construction plus a valid controlled query. Extraction, file access, and execution require separate capabilities and are unnecessary when the task is to identify/fix the construction. Verify a fix with a legitimate sort, a rejected raw expression, and unchanged literal-value behavior. [SQLite ORDER BY](https://www.sqlite.org/lang_select.html#orderby) and [Python binding API](https://docs.python.org/3/library/sqlite3.html) describe the example's engine/API.
