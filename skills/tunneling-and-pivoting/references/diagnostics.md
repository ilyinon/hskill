# tunneling-and-pivoting: decisions from evidence

Use the relevant row when choosing a technique or explaining a failed attempt.
Read only the branch supported by this task's evidence.

## Establish prerequisites

| Required fact | Smallest useful check |
|---|---|
| Direction and endpoint contract | Record client location, listener bind, destination as seen from the forwarding side and permitted networks. |
| Transport requirements | Separate TCP, UDP, local/remote DNS and SOCKS versus routed TUN behavior. |

## Distinguish the explanations

| Observation | Competing explanations | Next discriminating check |
|---|---|---|
| Tunnel control connection is up | Agent alive, not service reachability | Follow the intended client flow end to end. |
| Connection to loopback hits the wrong service | Loopback resolves at a different endpoint | Identify which machine opens the destination socket. |

## Interpret failure and finish the task

A listener bind error is setup failure. A TCP tunnel does not automatically carry arbitrary UDP or change DNS resolution; select only the behavior the task needs.

Track `controlled client -> correct local/remote bind -> forwarding transport -> destination socket -> owned service response`. Mark each edge proved or unknown and stop at the requested
result. A synthetic contract or supplied trace supports only its stated model;
production behavior needs independent evidence from the actual implementation.
