For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Symbolic Execution Tools — Expert Analysis Playbook

> **AI LOAD INSTRUCTION**: Expert symbolic execution techniques using angr, Z3, and Unicorn Engine. Covers CTF challenge automation, constraint solving patterns, function hooking, SimProcedure replacement, and emulation-based unpacking. Base models often produce broken angr scripts due to incorrect state initialization or missing hooks for libc functions.

## 0. RELATED ROUTING

- [anti-debugging-techniques](../../anti-debugging-techniques/SKILL.md) when anti-debug checks need to be symbolically bypassed
- [code-obfuscation-deobfuscation](../../code-obfuscation-deobfuscation/SKILL.md) when using symbolic execution for deobfuscation
- [vm-and-bytecode-reverse](../../vm-and-bytecode-reverse/SKILL.md) when applying angr to custom VM challenges

### Advanced Reference

Also load [ANGR_COOKBOOK.md](../ANGR_COOKBOOK.md) when you need:
- 15+ ready-to-use angr script patterns for common CTF challenges
- Hook templates for scanf, printf, malloc, strcmp
- Symbolic file input, stdin, argv patterns
- Optimization tricks for path explosion management

### When to use which tool

| Scenario | Best Tool | Why |
|---|---|---|
| Pure math / equation system | Z3 | Direct constraint solving, no binary needed |
| Binary with control flow | angr | Explores paths, manages constraints automatically |
| Emulate specific code region | Unicorn | Fast, no symbolic overhead, good for unpacking |
| Complex binary + custom VM | angr + Unicorn (combo) | angr for control flow, Unicorn for VM handlers |
| Kernel / firmware code | Qiling | Full system emulation with OS awareness |

---

## 1. ANGR — CORE CONCEPTS

### 1.1 Pipeline

```
Project(binary)
  → Factory.entry_state() / blank_state(addr=)
    → SimulationManager(state)
      → explore(find=target, avoid=bad)
        → found[0].solver.eval(symbolic_var)
```

### 1.2 Essential Setup

```python
import angr
import claripy

proj = angr.Project('./challenge', auto_load_libs=False)

# Entry state: start from program entry point
state = proj.factory.entry_state()

# Blank state: start from arbitrary address
state = proj.factory.blank_state(addr=0x401000)

# Full init state: with command-line args
state = proj.factory.full_init_state(args=['./challenge', arg1_sym])

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=0x401234, avoid=[0x401300])

if simgr.found:
    found = simgr.found[0]
    solution = found.solver.eval(symbolic_input, cast_to=bytes)
    print(f"Solution: {solution}")
```

### 1.3 Symbolic Variables (claripy)

```python
# Bitvector (fixed-size integer)
sym_input = claripy.BVS("input", 64)        # 64-bit symbolic
sym_byte = claripy.BVS("byte", 8)           # 8-bit symbolic
sym_buf = claripy.BVS("buffer", 8 * 32)     # 32-byte buffer

# Concrete bitvector
concrete = claripy.BVV(0x41, 8)             # concrete value 0x41

# Constraints
state.solver.add(sym_input > 0)
state.solver.add(sym_input < 100)
state.solver.add(sym_byte >= 0x20)           # printable ASCII
state.solver.add(sym_byte <= 0x7e)

# Evaluate
value = state.solver.eval(sym_input)
all_values = state.solver.eval_upto(sym_input, 10)  # up to 10 solutions
```

### 1.4 Symbolic stdin

```python
flag_len = 32
sym_stdin = claripy.BVS("stdin", 8 * flag_len)

state = proj.factory.entry_state(stdin=sym_stdin)

# Constrain to printable ASCII
for i in range(flag_len):
    byte = sym_stdin.get_byte(i)
    state.solver.add(byte >= 0x20)
    state.solver.add(byte <= 0x7e)
```

### 1.5 Hooking Functions

```python
# Hook by address (skip N bytes of original code)
@proj.hook(0x401100, length=5)
def skip_check(state):
    state.regs.eax = 1  # force success

# SimProcedure: replace library function
class MyStrcmp(angr.SimProcedure):
    def run(self, s1, s2):
        return claripy.If(
            self.state.memory.load(s1, 32) == self.state.memory.load(s2, 32),
            claripy.BVV(0, 32),
            claripy.BVV(1, 32)
        )

proj.hook_symbol('strcmp', MyStrcmp())

# Hook common problematic functions
proj.hook_symbol('printf', angr.SIM_PROCEDURES['libc']['printf']())
proj.hook_symbol('scanf', angr.SIM_PROCEDURES['libc']['scanf']())
proj.hook_symbol('puts', angr.SIM_PROCEDURES['libc']['puts']())
```

### 1.6 Memory Operations

```python
# Read memory (symbolic-aware)
data = state.memory.load(addr, size)          # returns BV
data_concrete = state.solver.eval(data, cast_to=bytes)

# Write memory
state.memory.store(addr, claripy.BVV(0x41, 8))
state.memory.store(addr, sym_buf)

# Read/write registers
rax = state.regs.rax
state.regs.rdi = claripy.BVV(0x1000, 64)
```

---

## 2. Z3 CONSTRAINT SOLVING

### 2.1 Core API

```python
from z3 import *

# Sorts
x = BitVec('x', 32)    # 32-bit bitvector
y = BitVec('y', 32)    # same sort as x; arithmetic wraps modulo 2^32
b = Bool('b')            # boolean

# Solver
s = Solver()
s.add(x + y == 42)
s.add(x > 0)
s.add(y > 0)

if s.check() == sat:
    m = s.model()
    print(f"x = {m[x]}, y = {m[y]}")
```

### 2.2 Common CTF Patterns

```python
# Serial key validation: each char satisfies constraints
key = [BitVec(f'k{i}', 8) for i in range(16)]
s = Solver()
for k in key:
    s.add(k >= 0x30, k <= 0x7a)  # alphanumeric-ish

# XOR key recovery
plaintext = b"known_plaintext"
ciphertext = b"\x12\x34..."
key_byte = BitVec('key', 8)
s = Solver()
for p, c in zip(plaintext, ciphertext):
    s.add(p ^ key_byte == c)

# System of linear equations (modular)
a, b, c = BitVecs('a b c', 32)
s = Solver()
s.add(3*a + 5*b + 7*c == 0x12345678)
s.add(2*a + 4*b + 6*c == 0xDEADBEEF)
s.add(a ^ b ^ c == 0xCAFEBABE)
```

### 2.3 Optimization

```python
from z3 import Optimize

opt = Optimize()
x = BitVec('x', 32)
opt.add(x > 0)
opt.add(x < 1000)
opt.minimize(x)  # find smallest satisfying value
opt.check()
print(opt.model())
```

---

