# anti-debugging-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 2. WINDOWS ANTI-DEBUG TECHNIQUES

### 2.1 IsDebuggerPresent / CheckRemoteDebuggerPresent

```c
if (IsDebuggerPresent()) ExitProcess(1);

BOOL debugged = FALSE;
CheckRemoteDebuggerPresent(GetCurrentProcess(), &debugged);
if (debugged) ExitProcess(1);
```

**Bypass**: Hook `kernel32!IsDebuggerPresent` to return 0, or patch PEB directly.

### 2.2 PEB Flags

| Field | Offset (x64) | Debugged Value | Normal Value |
|---|---|---|---|
| `BeingDebugged` | `PEB+0x02` | 1 | 0 |
| `NtGlobalFlag` | `PEB+0xBC` | `0x70` (FLG_HEAP_*) | 0 |
| `ProcessHeap.Flags` | Heap+0x40 | `0x40000062` | `0x00000002` |
| `ProcessHeap.ForceFlags` | Heap+0x44 | `0x40000060` | 0 |

```asm
mov rax, gs:[0x60]    ; PEB
movzx eax, byte [rax+0x02]  ; BeingDebugged
test eax, eax
jnz debugger_detected
```

**Bypass**: Zero all four fields. ScyllaHide does this automatically.

### 2.3 NtQueryInformationProcess

| InfoClass | Value | Debugged Return |
|---|---|---|
| `ProcessDebugPort` | 0x07 | Non-zero port |
| `ProcessDebugObjectHandle` | 0x1E | Valid handle |
| `ProcessDebugFlags` | 0x1F | 0 (inverted!) |

**Bypass**: Hook `ntdll!NtQueryInformationProcess` to return clean values per info class.

### 2.4 Hardware Breakpoint Detection

```c
CONTEXT ctx;
ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
GetThreadContext(GetCurrentThread(), &ctx);
if (ctx.Dr0 || ctx.Dr1 || ctx.Dr2 || ctx.Dr3)
    ExitProcess(1);
```

**Bypass**: Hook `GetThreadContext` to zero DR0–DR3, or use `NtSetInformationThread(ThreadHideFromDebugger)` preemptively (ironically, the anti-debug technique itself).

### 2.5 INT 2D / INT 3 / UD2 Exception Tricks

`INT 2D` is the kernel debug service interrupt. Without a debugger, it raises `STATUS_BREAKPOINT`; with a debugger, behavior differs (byte skipping).

```asm
xor eax, eax
int 2dh
nop          ; debugger may skip this byte
; ... divergent execution path ...
```

**Bypass**: Handle in VEH or patch the interrupt instruction.

### 2.6 TLS Callbacks

TLS callbacks execute before `main()` / `WinMain()`. Anti-debug checks placed here run before the debugger's initial break.

**Bypass**: In x64dbg, set "Break on TLS Callbacks" option. In WinDbg, use `sxe ld` to break on module load.

### 2.7 NtSetInformationThread(ThreadHideFromDebugger)

```c
NtSetInformationThread(GetCurrentThread(), ThreadHideFromDebugger, NULL, 0);
```

After this call, the thread becomes invisible to the debugger — breakpoints and single-stepping stop working silently.

**Bypass**: Hook `NtSetInformationThread` to NOP when `ThreadInfoClass == 0x11`.

### 2.8 VEH-Based Detection

Registers a Vectored Exception Handler that checks `EXCEPTION_RECORD` for debugger-specific behavior (single-step flag, guard page violations with debugger semantics).

**Bypass**: Understand the VEH logic and ensure the exception chain behaves identically to non-debugged execution.

---

## 3. ADVANCED MULTI-LAYER TECHNIQUES

### 3.1 Self-Debugging (fork + ptrace)

The process forks a child that attaches to the parent via ptrace. If an external debugger is already attached, the child's ptrace fails.

```c
pid_t child = fork();
if (child == 0) {
    if (ptrace(PTRACE_ATTACH, getppid(), 0, 0) == -1)
        kill(getppid(), SIGKILL);
    else
        ptrace(PTRACE_DETACH, getppid(), 0, 0);
    _exit(0);
}
wait(NULL);
```

**Bypass**: Patch the `fork()` return or kill/detach the watchdog child.

### 3.2 Multi-Process Debugging Detection

Parent and child cooperatively check each other's debug state, creating a mutual-watch pattern.

**Bypass**: Attach to both processes (GDB `follow-fork-mode`, or two debugger instances).

### 3.3 Timing-Based with Multiple Checkpoints

Distributes timing checks across multiple functions, comparing cumulative drift. Single patches fail because the total still exceeds threshold.

**Bypass**: Frida `Interceptor.replace` all timing sources (`rdtsc`, `clock_gettime`, `QueryPerformanceCounter`) to return controlled values.

### 3.4 Nanomite / INT3 Patching

Original conditional jumps are replaced with `INT3` (0xCC). A parent debugger process handles each `INT3`, evaluates the condition, and sets the child's EIP accordingly.

**Bypass**: Reconstruct the original jump table by tracing all `INT3` handlers, then patch the binary.

---

## 4. COUNTERMEASURE TOOLS

| Tool | Platform | Capability |
|---|---|---|
| **ScyllaHide** | Windows (x64dbg/IDA/OllyDbg) | Auto-patches PEB, hooks NtQuery*, hides threads, fixes timing |
| **TitanHide** | Windows (kernel driver) | Kernel-level hiding for all user-mode checks |
| **Frida** | Cross-platform | Script-based hooking of any function, timing spoofing |
| **LD_PRELOAD shims** | Linux | Replace ptrace, getenv, fopen at load time |
| **GDB scripts** | Linux | `catch syscall`, conditional BP, register fixup |
| **Qiling** | Cross-platform | Full-system emulation, bypass all hardware checks |

---

## 5. SYSTEMATIC BYPASS METHODOLOGY

```
Step 1: Static analysis — identify anti-debug calls
  └─ Search for: ptrace, IsDebuggerPresent, NtQuery, rdtsc,
     GetTickCount, SIGTRAP, INT 2D, TLS directory entries

Step 2: Classify each check
  ├─ API-based → hook or patch the call
  ├─ Flag-based → patch PEB/proc fields
  ├─ Timing-based → spoof time source
  ├─ Exception-based → forward/handle exception correctly
  └─ Multi-process → handle both processes

Step 3: Apply bypass (order matters)
  1. Load ScyllaHide / set LD_PRELOAD (covers 80% of checks)
  2. Handle TLS callbacks (break before main)
  3. Patch remaining custom checks (Frida or binary patch)
  4. Verify: run with breakpoints, confirm no premature exit

Step 4: Validate bypass completeness
  └─ Set BP on ExitProcess/exit/_exit — if hit unexpectedly,
     a check was missed → trace back from exit call
```

---

