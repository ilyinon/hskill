# cmdi-command-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Actual process invocation | Distinguish shell source from an executable plus argument vector and environment. |
| Argument policy | Identify option parsing, separators, working directory and the intended input type. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Shell punctuation is printed literally | No shell or correctly quoted shell data | Read the invocation and captured argv before changing punctuation. |
| Input starts with a dash | Ordinary filename or unintended utility option | Check a finite operand policy and where option parsing ends. |

## Interpret failure and finish the task

A local command-builder error did not reach the intended sink. A literal semicolon disproves that shell-syntax path but does not establish safe argument semantics.

Track `input -> invocation mode -> actual argv/interpreter -> intended operation -> bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
