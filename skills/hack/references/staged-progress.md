# Finish tasks whose evidence arrives in stages

Use when the requested result needs multiple tools or intermediate capabilities,
especially after an incomplete artifact, misleading lead, or failed operation.
Keep the user's completion criterion explicit; collecting several interesting
facts does not by itself finish the task.

At each useful checkpoint, retain only:

```text
requested end state | established capabilities | earliest missing dependency
last discriminating result | current conditions | next useful action | stop limit
```

An unavailable continuation is not an empty continuation. A malformed tool call
does not test the hypothesis. Preserve the failure, inspect the tool's expected
representation or available fallback, and resume from the missing observation.
Avoid replaying all earlier successful steps after a context reset.

When a decoy seems promising, ask whether it connects to the requested object and
current consumer. Stop spending on it after a valid negative or a broken joining
contract unless new evidence predicts a different result. If the environment
changes mid-task, recheck affected dependencies before using the old conclusion.

Before finishing, produce the requested value, bounded finding, verified repair,
or other concrete deliverable and check it against the supplied construction.
If scope or missing evidence prevents completion, identify the exact broken edge
and useful partial result. A description of how someone could finish is not the
requested recovered artifact.

For training and evaluation, use progressive observations with meaningful choices,
an incomplete input, a plausible alternative, and at least one recoverable tool
failure. Grade final task completion and evidence quality before simulated action
cost. Count redundant or uninformative actions separately; a necessary negative
check is useful work. Offline recordings and small models exercise reasoning
under their stated construction, not real product behavior.
