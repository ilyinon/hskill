# memory-forensics-volatility technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 4. LINUX MEMORY ANALYSIS

```bash
# Vol2 (requires Linux profile)
vol.py -f mem.lime --profile=LinuxProfile linux_pslist
vol.py -f mem.lime --profile=LinuxProfile linux_pstree
vol.py -f mem.lime --profile=LinuxProfile linux_netstat
vol.py -f mem.lime --profile=LinuxProfile linux_bash        # bash history
vol.py -f mem.lime --profile=LinuxProfile linux_enumerate_files
vol.py -f mem.lime --profile=LinuxProfile linux_proc_maps -p PID
vol.py -f mem.lime --profile=LinuxProfile linux_malfind

# Vol3
vol -f mem.lime linux.pslist
vol -f mem.lime linux.pstree
vol -f mem.lime linux.bash
vol -f mem.lime linux.check_afinfo     # rootkit detection
vol -f mem.lime linux.check_syscall    # syscall hooking
vol -f mem.lime linux.tty_check        # TTY hooking
```

### Building Linux Profiles (Vol2)

```bash
cd volatility/tools/linux
make
# Creates module.dwarf + System.map → zip as profile
zip LinuxProfile.zip module.dwarf /boot/System.map-$(uname -r)
# Place in volatility/plugins/overlays/linux/
```

---

## 5. MALWARE INDICATORS IN MEMORY

| Indicator | Detection Method | What It Means |
|---|---|---|
| Process in psscan but not pslist | Compare pslist vs psscan | DKOM — process hiding |
| Unexpected parent-child | pstree analysis | e.g., svchost spawned by cmd.exe |
| MZ header in non-image memory | malfind | Reflective DLL / PE injection |
| RWX memory without backing file | malfind | Shellcode injection |
| DLL unlinked from all PEB lists | ldrmodules (all False) | Stealth DLL loading |
| svchost.exe not child of services.exe | pstree | Fake svchost (malware) |
| Unusual network connections | netscan + PID correlation | C2 communication |
| Hooking in SSDT/IDT | ssdt / idt plugins | Rootkit |
| Modified kernel objects | linux_check_syscall | Linux rootkit |

### Normal Parent-Child Relationships (Windows)

```
System (4)
└── smss.exe
    └── csrss.exe
    └── wininit.exe
        └── services.exe
            └── svchost.exe (multiple)
            └── spoolsv.exe
        └── lsass.exe
    └── winlogon.exe
        └── explorer.exe
            └── user applications
```

---

## 6. DECISION TREE

```
Memory dump acquired — need to analyze
│
├── What OS?
│   ├── Windows → vol imageinfo / windows.info (§3 Step 1)
│   └── Linux → build profile or use Vol3 auto-detect (§4)
│
├── Malware investigation?
│   ├── Check processes: pslist vs psscan (hidden?) (§3 Step 2)
│   ├── Check parent-child: pstree (suspicious spawning?) (§5)
│   ├── Check injections: malfind (RWX memory?) (§3 Step 5)
│   ├── Check DLLs: ldrmodules (unlinked?) (§3 Step 4)
│   ├── Check network: netscan (C2 connections?) (§3 Step 3)
│   └── Extract suspicious files: dumpfiles (§3 Step 7)
│
├── Credential recovery?
│   ├── SAM hashes → hashdump (§3 Step 6)
│   ├── LSA secrets → lsadump (§3 Step 6)
│   ├── Cached domain creds → cachedump (§3 Step 6)
│   └── Plaintext passwords → mimikatz plugin (§3 Step 6)
│
├── Incident timeline?
│   ├── timeliner for comprehensive timeline (§3 Step 10)
│   ├── cmdscan / consoles for command history (§3 Step 9)
│   ├── userassist for program execution (§3 Step 8)
│   └── Cross-reference with PCAP timeline (→ traffic-analysis-pcap)
│
├── CTF / flag hunting?
│   ├── filescan + grep for flag patterns (§3 Step 7)
│   ├── cmdscan for typed flags/passwords (§3 Step 9)
│   ├── Clipboard: clipboard plugin
│   ├── Screenshots: screenshot plugin
│   └── Environment vars: envars plugin
│
└── Linux-specific?
    ├── linux_bash for shell history (§4)
    ├── linux_check_syscall for rootkit (§4)
    └── linux_netstat for connections (§4)
```
