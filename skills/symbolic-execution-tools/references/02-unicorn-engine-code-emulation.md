# symbolic-execution-tools technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 3. UNICORN ENGINE — CODE EMULATION

### 3.1 Basic Setup

```python
from unicorn import *
from unicorn.x86_const import *
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

mu = Uc(UC_ARCH_X86, UC_MODE_64)

CODE_ADDR = 0x400000
STACK_ADDR = 0x7fff0000
STACK_SIZE = 0x10000

mu.mem_map(CODE_ADDR, 0x10000)
mu.mem_map(STACK_ADDR, STACK_SIZE)

mu.mem_write(CODE_ADDR, code_bytes)
mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE - 0x1000)
mu.reg_write(UC_X86_REG_RBP, STACK_ADDR + STACK_SIZE - 0x1000)

mu.emu_start(CODE_ADDR, CODE_ADDR + len(code_bytes))

result = mu.reg_read(UC_X86_REG_RAX)
```

### 3.2 Hooking Memory & Instructions

```python
# Hook memory access
def hook_mem(uc, access, address, size, value, user_data):
    if access == UC_MEM_WRITE:
        print(f"Write {value:#x} to {address:#x}")
    elif access == UC_MEM_READ:
        print(f"Read from {address:#x}")

mu.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, hook_mem)

# Hook specific instruction (for tracing)
def hook_code(uc, address, size, user_data):
    code = uc.mem_read(address, size)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for insn in md.disasm(bytes(code), address):
        print(f"  {insn.address:#x}: {insn.mnemonic} {insn.op_str}")

mu.hook_add(UC_HOOK_CODE, hook_code)
```

### 3.3 Use Cases

| Use Case | Approach |
|---|---|
| Unpack shellcode | Map shellcode, emulate, dump decoded payload |
| Decrypt strings | Emulate decryption function with controlled inputs |
| Brute-force short keys | Loop emulation with different key inputs |
| Analyze obfuscated function | Emulate function, observe register/memory state |
| Firmware code emulation | Map firmware memory layout, emulate routines |

---

## 4. ANGR EXPLORATION STRATEGIES

### 4.1 find/avoid

```python
simgr.explore(
    find=lambda s: b"Correct" in s.posix.dumps(1),   # stdout contains "Correct"
    avoid=lambda s: b"Wrong" in s.posix.dumps(1)      # avoid "Wrong" output
)
```

### 4.2 Managing Path Explosion

| Strategy | Implementation |
|---|---|
| Constrain input space | Add constraints (printable, length limits) |
| Avoid dead-end paths | Use `avoid=` for known failure addresses |
| Hook complex functions | Replace with simplified SimProcedure |
| Limit loop iterations | `simgr.use_technique(angr.exploration_techniques.LoopSeer(bound=10))`; choose a bound consistent with the real program |
| Use veritesting | `simgr.use_technique(angr.exploration_techniques.Veritesting())` |
| DFS instead of BFS | `simgr.use_technique(angr.exploration_techniques.DFS())` |
| Timeout per path | `simgr.explore(..., num_find=1)` + timeout wrapper |

### 4.3 Concrete + Symbolic Hybrid

```python
state = proj.factory.entry_state(
    add_options={angr.options.UNICORN}  # use Unicorn for concrete regions
)
```

This dramatically speeds up execution: concrete code runs natively via Unicorn, switching to symbolic only when symbolic variables are involved.

---

## 5. PRACTICAL WORKFLOW

### 5.1 CTF Binary Solving Workflow

```
1. Static analysis: identify input method, success/fail conditions
   └─ Find "Correct" / "Wrong" strings → get their xref addresses

2. Choose tool:
   ├─ Pure math (no binary needed) → Z3
   ├─ Small binary, clear success/fail → angr explore
   └─ Specific function to emulate → Unicorn

3. Set up symbolic input:
   ├─ stdin → claripy.BVS + entry_state(stdin=)
   ├─ argv → full_init_state(args=[...])
   ├─ file input → SimFile
   └─ specific memory → state.memory.store(addr, sym)

4. Hook problematic functions:
   ├─ printf/puts → SimProcedure or no-op
   ├─ scanf → custom handler
   ├─ time/random → return concrete value
   └─ anti-debug → skip entirely

5. Explore and extract:
   └─ simgr.explore(find=, avoid=) → solver.eval()
```

---

## 6. DECISION TREE

```
Need to solve a reversing challenge?
│
├─ Is the challenge pure math / equations?
│  └─ Yes → Z3
│     ├─ Linear equations → BitVec + Solver
│     ├─ Modular arithmetic → BitVec (natural mod 2^n)
│     ├─ Boolean logic → Bool + Solver
│     └─ Optimization → Optimize + minimize/maximize
│
├─ Is it a compiled binary with clear success/fail?
│  └─ Yes → angr
│     ├─ Input via stdin → symbolic stdin
│     ├─ Input via argv → full_init_state with symbolic args
│     ├─ Input via file → SimFile
│     ├─ Path explosion → add constraints, avoid paths, hook loops
│     └─ Complex library calls → hook with SimProcedure
│
├─ Need to emulate a specific function/region?
│  └─ Yes → Unicorn Engine
│     ├─ Decryption routine → map code + data, emulate, read result
│     ├─ Shellcode analysis → map shellcode, hook syscalls
│     └─ Key schedule → emulate with different inputs
│
├─ Need to analyze firmware / exotic arch?
│  └─ Yes → Qiling (full system emulation with OS support)
│
├─ Binary has VM protection?
│  └─ angr for handler analysis + Z3 for bytecode constraints
│
└─ None of the above working?
   ├─ Combine: Unicorn for concrete regions + Z3 for constraints
   ├─ Manual reverse engineering with debugger
   └─ Side-channel approach (timing, power analysis for hardware)
```

---

## 7. COMMON PITFALLS & FIXES

| Problem | Cause | Fix |
|---|---|---|
| angr hangs forever | Path explosion in loops | Add `avoid=` for loop-back edges, or hook the loop |
| Z3 returns `unknown` | Non-linear constraints too complex | Simplify, split into sub-problems, use `set_param("timeout", 5000)` |
| Unicorn crashes on syscall | Syscall not handled | Hook syscall interrupt, handle or skip |
| angr wrong result | Incorrect state initialization | Verify initial memory layout matches actual binary |
| Symbolic memory too large | Unbounded symbolic reads | Concretize array indices where possible |
| SimProcedure wrong types | Argument type mismatch | Check calling convention (cdecl vs fastcall) |
| angr can't load binary | Missing libraries | Use `auto_load_libs=False` + hook needed symbols |

---

## 8. TOOL VERSIONS & INSTALLATION

```bash
# angr (Python 3.8+)
pip install angr

# Z3
pip install z3-solver

# Unicorn Engine
pip install unicorn

# Capstone (disassembly, pairs with Unicorn)
pip install capstone

# Keystone (assembly)
pip install keystone-engine
```
