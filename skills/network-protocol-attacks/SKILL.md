---
name: network-protocol-attacks
description: >-
  Network protocol attack playbook. Use when exploiting layer 2/3 protocols including ARP spoofing, LLMNR/NBT-NS/mDNS poisoning, WPAD abuse, DHCPv6 attacks, VLAN hopping, STP manipulation, DNS spoofing, IPv6 attacks, and IDS/IPS evasion.
---

# Network Protocol Attacks

## Working approach

- Map segment, protocols, trust assumptions, protections, and permitted test hosts
- Choose the specific discovery, naming, switching, or address-assignment hypothesis
- Use bounded controlled traffic and verify the receiving peer's actual behavior.

## Evidence and limits

The test crosses the intended network identity, routing, or confidentiality boundary with captured evidence.

Receiving a broadcast or sending a spoofed packet does not establish interception; signing, DHCP protections, client policy, and network position matter.

## Solving decisions

For unclear prerequisites or failed attempts, use [diagnostics](./references/diagnostics.md). Read the [worked case](./references/worked-cases.md) when a change of approach needs an example; recheck its assumptions.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. ARP SPOOFING; 2. LLMNR / NBT-NS / mDNS POISONING; 3. WPAD ABUSE; 4. DHCPv6 ATTACK — mitm6; 5. VLAN HOPPING; 6. STP MANIPULATION | [Read](./references/01-arp-spoofing.md) |
| 7. DNS SPOOFING; 8. IPv6 ATTACKS; 9. IDS/IPS EVASION; 10. DECISION TREE | [Read](./references/02-dns-spoofing.md) |
| Advanced: NAME RESOLUTION POISONING — Responder & mitm6 Deep Dive | [Read](./NAME_RESOLUTION_POISONING.md) |
