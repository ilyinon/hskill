# anti-debugging-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. DECISION TREE

```
Binary exits/crashes under debugger?
│
├─ Crashes immediately before main?
│  └─ TLS callback anti-debug
│     └─ Enable TLS callback breaking in debugger
│
├─ Crashes at startup?
│  ├─ Linux: check for ptrace(TRACEME)
│  │  └─ LD_PRELOAD hook or NOP patch
│  └─ Windows: check IsDebuggerPresent / PEB
│     └─ ScyllaHide or manual PEB patch
│
├─ Crashes after some execution?
│  ├─ Consistent crash point → API-based check
│  │  ├─ NtQueryInformationProcess → hook return values
│  │  ├─ /proc/self/status → filter TracerPid
│  │  └─ Hardware BP detection → hook GetThreadContext
│  │
│  ├─ Variable crash point → timing-based check
│  │  └─ Hook rdtsc / QueryPerformanceCounter
│  │
│  └─ Crash on breakpoint hit → exception-based check
│     ├─ INT 2D / INT 3 trick → handle in VEH
│     └─ SIGTRAP handler → GDB: handle SIGTRAP pass
│
├─ Debugger loses control silently?
│  └─ ThreadHideFromDebugger
│     └─ Hook NtSetInformationThread
│
├─ Child process detects and kills parent?
│  └─ Self-debugging (fork+ptrace)
│     └─ Patch fork() or handle both processes
│
└─ All basic bypasses applied but still detected?
   └─ Multi-layer / custom checks
      ├─ Use Frida for comprehensive API hooking
      ├─ Full emulation with Qiling
      └─ Trace all calls to exit/abort to find remaining checks
```

---

## 7. CTF & REAL-WORLD PATTERNS

### Common CTF Anti-Debug Patterns

| Pattern | Frequency | Quick Bypass |
|---|---|---|
| Single `ptrace(TRACEME)` | Very common | `LD_PRELOAD` one-liner |
| `IsDebuggerPresent` + `NtGlobalFlag` | Common | ScyllaHide |
| rdtsc timing in loop | Moderate | Patch comparison threshold |
| signal(SIGTRAP) + raise | Moderate | GDB signal forwarding |
| fork + ptrace watchdog | Rare but tricky | Kill child or patch fork |
| Nanomite INT3 replacement | Rare (advanced) | Reconstruct jump table |

### Real-World Protections

| Protector | Primary Anti-Debug | Recommended Tool |
|---|---|---|
| VMProtect | PEB + timing + driver-level | TitanHide + ScyllaHide |
| Themida | Multi-layer PEB + SEH + timing | ScyllaHide + manual patches |
| Enigma Protector | IsDebuggerPresent + CRC checks | x64dbg + ScyllaHide |
| UPX (custom) | Usually none (just packing) | Standard unpack |
| Custom (malware) | Varies widely | Frida + Qiling for analysis |

---

## 8. QUICK REFERENCE — BYPASS CHEAT SHEET

### Linux One-Liners

```bash
# LD_PRELOAD anti-ptrace
echo 'long ptrace(int r, ...) { return 0; }' > /tmp/ap.c
gcc -shared -o /tmp/ap.so /tmp/ap.c
LD_PRELOAD=/tmp/ap.so ./target

# GDB: catch and bypass ptrace
(gdb) catch syscall ptrace
(gdb) commands
> set $rax = 0
> continue
> end
```

### Frida Anti-Debug Bypass (Cross-Platform)

```javascript
// Hook IsDebuggerPresent (Windows)
Interceptor.replace(
  Module.getExportByName('kernel32.dll', 'IsDebuggerPresent'),
  new NativeCallback(() => 0, 'int', [])
);

// Hook ptrace (Linux)
Interceptor.replace(
  Module.getExportByName(null, 'ptrace'),
  new NativeCallback(() => 0, 'long', ['int', 'int', 'pointer', 'pointer'])
);

// Timing spoof
Interceptor.attach(Module.getExportByName(null, 'clock_gettime'), {
  onLeave(retval) {
    // manipulate timespec to hide debugger delay
  }
});
```

### x64dbg ScyllaHide Quick Setup

1. Plugins → ScyllaHide → Options
2. Check: PEB BeingDebugged, NtGlobalFlag, HeapFlags
3. Check: NtQueryInformationProcess (all classes)
4. Check: NtSetInformationThread (HideFromDebugger)
5. Check: GetTickCount, QueryPerformanceCounter
6. Apply → restart debugging session
