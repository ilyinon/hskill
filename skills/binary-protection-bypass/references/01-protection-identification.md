For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Binary Protection Bypass — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert binary protection identification and bypass techniques. Covers ASLR, PIE, NX, RELRO, canary, FORTIFY_SOURCE, stack clash, CET shadow stack, and ARM MTE. Each protection is paired with its bypass methods and required primitives. Distilled from ctf-wiki mitigation sections and real-world exploitation. Base models often confuse which protections block which attacks and miss the combinatorial effect of multiple protections.

## 0. RELATED ROUTING

- [stack-overflow-and-rop](../../stack-overflow-and-rop/SKILL.md) — ROP chains to bypass NX, ret2libc for ASLR bypass
- [format-string-exploitation](../../format-string-exploitation/SKILL.md) — primary method for leaking canary, PIE, libc addresses
- [heap-exploitation](../../heap-exploitation/SKILL.md) — heap attacks for RELRO bypass (when GOT is read-only)
- [arbitrary-write-to-rce](../../arbitrary-write-to-rce/SKILL.md) — what to overwrite when GOT is protected by RELRO

### Advanced Reference

Load [PROTECTION_BYPASS_MATRIX.md](../PROTECTION_BYPASS_MATRIX.md) for comprehensive protection × bypass × primitive matrix.

---

## 1. PROTECTION IDENTIFICATION

```bash
$ checksec ./binary
[*] '/path/to/binary'
    Arch:     amd64-64-little
    RELRO:    Full RELRO          ← GOT read-only
    Stack:    Canary found        ← stack canary enabled
    NX:       NX enabled          ← stack not executable
    PIE:      PIE enabled         ← position-independent code
    FORTIFY:  Enabled             ← fortified libc functions
```

### Quick Identification Table

| Protection | Check Command | Binary Indicator |
|---|---|---|
| ASLR | `cat /proc/sys/kernel/randomize_va_space` | OS-level (0=off, 1=partial, 2=full) |
| PIE | `checksec` or `readelf -h` (Type: DYN) | Binary compiled with `-pie` |
| NX | `checksec` or `readelf -l` (no RWE segment) | `gcc -z noexecstack` (default on) |
| Canary | `checksec` or look for `__stack_chk_fail@plt` | `gcc -fstack-protector-all` |
| Partial RELRO | `readelf -l` (GNU_RELRO segment, `.got.plt` writable) | `gcc -Wl,-z,relro` |
| Full RELRO | `readelf -l` + `.got` section read-only | `gcc -Wl,-z,relro,-z,now` |
| FORTIFY | Presence of `__printf_chk`, `__memcpy_chk` etc. | `gcc -D_FORTIFY_SOURCE=2` |

---

## 2. ASLR BYPASS

ASLR randomizes base addresses of stack, heap, libc, and mmap regions at each execution.

| Bypass Method | Required Primitive | Notes |
|---|---|---|
| Information leak | Any read primitive (format string, OOB read, UAF) | Leak libc/stack/heap address → calculate base |
| Partial overwrite | Write primitive (limited length) | Overwrite last 1-2 bytes (page offset fixed) |
| Brute force (32-bit) | Ability to reconnect/retry | ~256–4096 attempts (8-12 bits entropy) |
| Return-to-PLT | Stack overflow | PLT addresses are at fixed offset from binary base (if no PIE) |
| ret2dlresolve | Stack overflow + write primitive | Resolve arbitrary function without knowing libc base |
| Format string leak | Format string vulnerability | `%N$p` for stack/libc/heap addresses |
| Stack reading | Byte-by-byte (fork server) | Read stack byte-by-byte via crash oracle |

### ASLR Entropy (x86-64 Linux)

| Region | Entropy (bits) | Positions |
|---|---|---|
| Stack | 22 | ~4M |
| mmap / libc | 28 | ~256M |
| Heap (brk) | 13 | ~8K |
| PIE binary | 28 | ~256M |

---

## 3. PIE BYPASS

PIE (Position Independent Executable) randomizes the binary's own code/data base address.

| Bypass Method | Required Primitive | Notes |
|---|---|---|
| Information leak | Read return address from stack | PIE base = leaked_addr - known_offset |
| Partial overwrite | One-byte or two-byte write | Last 12 bits of page offset are fixed |
| Format string leak | Format string vulnerability | `%N$p` where N points to .text return address |
| Relative addressing | Knowledge of binary layout | If you know relative offsets, only need one leak |

### Partial Overwrite Details

```
PIE binary loaded at: 0x555555554000 (example)
Function at offset 0x1234: 0x555555555234

Overwrite return address last 2 bytes: 0x?234 → 0x?XXX
Unknown: bits 12-15 (one nibble = 4 bits = 16 possibilities)
Success rate: 1/16 per attempt
```

---

## 4. NX / DEP BYPASS

NX (No-eXecute) / DEP (Data Execution Prevention) prevents execution of code on the stack/heap.

| Bypass Method | Detail |
|---|---|
| ROP (Return-Oriented Programming) | Chain existing code gadgets ending in `ret` |
| ret2libc | Call libc functions (system, execve) directly |
| ret2csu | Use `__libc_csu_init` gadgets for controlled function calls |
| ret2dlresolve | Forge dynamic linker structures to resolve arbitrary functions |
| SROP | Use sigreturn to set all registers from fake signal frame |
| mprotect ROP | Chain mprotect(addr, size, PROT_RWX) → make page executable → jump to shellcode |
| JIT spray | In JIT environments (V8, etc.), create executable code via JIT compiler |

### mprotect Chain

```python
# Make stack executable, then jump to shellcode
rop = b'A' * offset
rop += p64(pop_rdi) + p64(stack_page)     # page-aligned address
rop += p64(pop_rsi) + p64(0x1000)         # size
rop += p64(pop_rdx) + p64(7)              # PROT_READ|PROT_WRITE|PROT_EXEC
rop += p64(mprotect_addr)
rop += p64(shellcode_addr)                 # jump to shellcode on now-executable stack
```

---

## 5. RELRO BYPASS

| RELRO Level | GOT Status | Bypass |
|---|---|---|
| No RELRO | GOT fully writable | Direct GOT overwrite |
| Partial RELRO | `.got.plt` writable (lazy binding) | GOT overwrite still works |
| Full RELRO | All GOT entries resolved at load, GOT read-only | Cannot write GOT → target other structures |

### Full RELRO Alternative Targets

| Target | When | How |
|---|---|---|
| `__malloc_hook` | glibc < 2.34 | Overwrite with one_gadget |
| `__free_hook` | glibc < 2.34 | Overwrite with `system`, trigger `free("/bin/sh")` |
| `_IO_FILE vtable` | Any glibc | FSOP / vtable hijack |
| `__exit_funcs` | Any glibc | Overwrite exit handler list |
| `TLS_dtor_list` | glibc ≥ 2.34 | Thread-local destructor list (needs pointer guard) |
| `.fini_array` | If writable | Overwrite destructor function pointers |
| Stack return address | Direct stack write | Overwrite return address for ROP |

See [arbitrary-write-to-rce](../../arbitrary-write-to-rce/SKILL.md) for comprehensive target list.

---

