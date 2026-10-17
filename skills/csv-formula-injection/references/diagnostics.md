# csv-formula-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| End-to-end spreadsheet workflow | Record export bytes, import options, product/version/locale and resulting cell type. |
| Safe claimed effect | Use inert arithmetic; distinguish formula evaluation, text, warning and external action. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| CSV field is quoted | CSV structure protected or cell forced to text | Reopen/import through the target workflow and inspect cell type. |
| Cell displays 2 | Evaluated =1+1, literal number 2, or cached value | Inspect formula/type and source mapping, not display alone. |

## Interpret failure and finish the task

An import error did not test formula handling. A warning or blocked external function is not command execution; do not generalize apostrophe/tab behavior across importers.

Track `user value -> export encoding -> importer cell typing -> evaluated or literal cell -> bounded consequence`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
