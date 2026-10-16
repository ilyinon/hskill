# arbitrary-write-to-rce technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 12. DECISION TREE

```
You have an arbitrary write primitive. What to target?

├── What's the RELRO level?
│   ├── None / Partial → GOT overwrite (simplest, most reliable)
│   │   └── printf→system, free→system, atoi→system
│   └── Full RELRO → GOT read-only, choose alternative:
│
├── What glibc version?
│   ├── < 2.34 (hooks available)
│   │   ├── __free_hook = system → free("/bin/sh") [easiest]
│   │   ├── __malloc_hook = one_gadget → trigger malloc [if constraints met]
│   │   └── __realloc_hook + __malloc_hook realloc trick [adjust stack alignment]
│   │
│   ├── ≥ 2.34 (no hooks)
│   │   ├── Know pointer guard (fs:[0x30])?
│   │   │   ├── YES → __exit_funcs or TLS_dtor_list
│   │   │   └── NO → overwrite pointer guard to 0 first, then exit_funcs
│   │   ├── _IO_FILE + _IO_wfile_jumps (House of Apple 2 / Cat)
│   │   │   └── Need: libc base + heap address + controllable FILE structure
│   │   ├── _dl_fini link_map corruption
│   │   │   └── Need: ld.so base address
│   │   └── .fini_array (if writable)
│   │       └── Need: binary base (no PIE, or PIE base leaked)
│   │
│   └── Any version
│       ├── Stack return address (if stack address known)
│       └── C++ vtable (if targeting C++ object with virtual functions)
│
├── Kernel write primitive?
│   ├── modprobe_path (simplest kernel→root)
│   ├── core_pattern (/proc/sys/kernel/core_pattern)
│   └── Direct cred structure overwrite
│
└── Need to chain read → write → execute?
    └── setcontext gadget: arbitrary write → pivot RSP → ROP chain
        ├── glibc < 2.29: setcontext+53 (uses RDI)
        └── glibc ≥ 2.29: setcontext+61 (uses RDX, need mov rdx, [rdi] gadget)
```
