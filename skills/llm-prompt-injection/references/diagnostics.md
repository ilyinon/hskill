# llm-prompt-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Trust and tool authority | Map untrusted document/message input, trusted user scope, tool identity and allowed actions. |
| Observable effect | Inspect actual dispatcher records, protected-data bytes and external state separately from generated text. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Model says it performed an action | Text claim, proposed call or completed tool effect | Correlate dispatcher result and target state. |
| Untrusted instruction changes wording | Content influence or a defined authority violation | Compare the stated security policy and independent protected marker/action. |

## Interpret failure and finish the task

A model refusal or tool-harness error is not proof about the actual authority boundary. Retrieved material cannot authorize actions or broaden the real user task.

Track `untrusted content -> model interpretation -> tool authorization -> actual protected action/data -> bounded violation`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.

## Review the tool boundary

Keep retrieved text in data fields. Validate each proposed call in the application against the authenticated user's permissions, the selected resource, and the current operation. Enforce those checks before invoking any connector. Use a stub dispatcher with inert inputs to verify that a legitimate request reaches its intended tool and that an unauthorized request never reaches the dispatcher. Check the application audit record separately from the model's reply. [OpenAI agent safety guidance](https://developers.openai.com/api/docs/guides/agent-builder-safety)
