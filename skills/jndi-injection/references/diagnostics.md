# jndi-injection: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Reachable lookup and provider | Trace caller input into InitialContext lookup and identify actual JDK/provider/classpath. |
| Reconstruction permissions | Separate outbound naming lookup, returned data, factories and any execution hook. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| DNS/LDAP observation exists | Lookup occurred, not necessarily reconstruction | Inspect client attribution and the next factory/return stage. |
| Factory/class is missing | Chain prerequisite absent or different local path | Check actual classpath/filter rather than regenerating the same payload. |

## Interpret failure and finish the task

A class-not-found or blocked remote factory leaves execution unproved. A tool callback is not attributable application behavior without source/log correlation.

Track `controlled name -> attributable lookup -> permitted object reconstruction -> bounded effect`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
