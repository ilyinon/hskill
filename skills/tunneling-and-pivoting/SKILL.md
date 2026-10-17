---
name: tunneling-and-pivoting
description: >-
  Tunneling and pivoting playbook. Use when establishing network tunnels through compromised hosts including SSH tunneling, Chisel, Ligolo-ng, socat, DNS/ICMP/HTTP tunneling, ProxyChains, and multi-layer pivoting strategies.
---

# Tunneling And Pivoting

## Working approach

- Record permitted source/destination networks, egress, transport, privileges, and required TCP/UDP/DNS behavior
- Choose one compatible forwarding/routing mechanism
- Verify route direction, bind address, authentication, and cleanup with an owned endpoint.

## Evidence and limits

The intended controlled client reaches the specified permitted service through the documented path.

A listening port or connected agent does not prove routing; SOCKS, transparent TUN routing, name resolution, and remote/local forwarding have different semantics.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. SSH TUNNELING; 2. CHISEL; 3. LIGOLO-NG; 4. SOCAT; 5. PROXYCHAINS / PROXIFIER | [Read](./references/01-ssh-tunneling.md) |
| 6. WINDOWS PIVOTING; 7. DNS TUNNELING; 8. ICMP TUNNELING; 9. HTTP TUNNELING; 10. PIVOTING DECISION MATRIX; 11. DECISION TREE | [Read](./references/02-windows-pivoting.md) |
