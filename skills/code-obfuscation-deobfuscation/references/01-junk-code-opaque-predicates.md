For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: Code Obfuscation & Deobfuscation — Expert Analysis Playbook

> **AI LOAD INSTRUCTION**: Expert techniques for identifying, classifying, and defeating code obfuscation in native binaries. Covers junk code, opaque predicates, SMC, control flow flattening, movfuscator, VM protectors (VMProtect/Themida/Code Virtualizer), string encryption, import hiding, and anti-disassembly tricks. Base models often conflate packing with obfuscation and miss the distinction between static and dynamic deobfuscation strategies.

## 0. RELATED ROUTING

- [anti-debugging-techniques](../../anti-debugging-techniques/SKILL.md) when the obfuscated binary also has anti-debug layers
- [symbolic-execution-tools](../../symbolic-execution-tools/SKILL.md) when using angr/Z3 for automated deobfuscation
- [vm-and-bytecode-reverse](../../vm-and-bytecode-reverse/SKILL.md) for deep VM protector bytecode analysis

### Quick identification picks

| Symptom in IDA/Ghidra | Likely Obfuscation | Start With |
|---|---|---|
| Flat CFG, single giant switch | Control flow flattening | Symbolic execution to recover CFG |
| Only `mov` instructions | movfuscator | demovfuscation / trace-based lifting |
| pushad/pushfd → VM entry | VM protector | Handler table extraction |
| XOR loop before code execution | SMC / string encryption | Dynamic analysis, breakpoint after decode |
| Impossible conditions (opaque predicates) | Junk code insertion | Pattern-based removal |
| All strings unreadable | String encryption | Hook decryption routine, or emulate |
| No imports in IAT | Import hiding | Trace GetProcAddress / hash resolution |

---

## 1. JUNK CODE & OPAQUE PREDICATES

### 1.1 Junk Code Insertion

Dead code that never affects program output, added to increase analysis time.

**Identification**:
- Instructions that write to registers/memory never read afterward
- Function calls whose return values are discarded and have no side effects
- Loops with invariant bounds that compute unused results

**Removal strategy**:
1. Compute def-use chains (IDA/Ghidra data flow analysis)
2. Mark instructions with no downstream use as dead
3. Verify removal doesn't change program behavior (trace comparison)

### 1.2 Opaque Predicates

Conditional branches where the condition is always true or always false, but this is non-obvious.

| Type | Example | Always Evaluates To |
|---|---|---|
| Arithmetic | `x² ≥ 0` | True |
| Number theory | `x*(x+1) % 2 == 0` | True (product of consecutive ints) |
| Pointer-based | `ptr == ptr` after aliasing | True |
| Hash-based | `CRC32(constant) == known_value` | True |

**Deobfuscation**:
- Abstract interpretation: prove the condition is constant
- Symbolic execution: Z3 proves `∀x: predicate(x) = True`
- Pattern matching: recognize known opaque predicate families
- Dynamic: trace and observe the branch is never taken / always taken

```python
import z3
x = z3.BitVec('x', 32)
s = z3.Solver()
s.add(x * (x + 1) % 2 != 0)
print(s.check())  # unsat → always true
```

---

## 2. SELF-MODIFYING CODE (SMC)

Runtime code patching: encrypted code is decrypted just before execution.

### 2.1 XOR Decryption Loop (Most Common)

```asm
lea esi, [encrypted_code]
mov ecx, code_length
mov al, xor_key
decrypt_loop:
    xor byte [esi], al
    inc esi
    loop decrypt_loop
    jmp encrypted_code  ; now decrypted
```

### 2.2 Analysis Strategy

```
1. Identify the decryption routine (look for XOR/ADD/SUB in loops writing to .text)
2. Set breakpoint AFTER the loop completes
3. At breakpoint: dump the decrypted memory region
4. Re-analyze the dumped code in IDA/Ghidra
5. For multi-layer: repeat for each decryption stage
```

### 2.3 Automated Unpacking via Emulation

```python
from unicorn import *
from unicorn.x86_const import *

mu = Uc(UC_ARCH_X86, UC_MODE_32)
mu.mem_map(0x400000, 0x10000)
mu.mem_write(0x400000, binary_code)
mu.emu_start(decrypt_entry, decrypt_end)
decrypted = mu.mem_read(code_start, code_length)
```

---

## 3. CONTROL FLOW FLATTENING (CFF)

### 3.1 Structure

Original sequential blocks are transformed into a dispatcher loop:

```
Original:      A → B → C → D

Flattened:     ┌──────────────────┐
               │   dispatcher     │
               │   switch(state)  │◄─────┐
               ├──────────────────┤      │
               │ case 1: block A  │──────┤
               │ case 2: block B  │──────┤
               │ case 3: block C  │──────┤
               │ case 4: block D  │──────┘
               └──────────────────┘
```

Each block sets `state = next_state` before jumping back to the dispatcher.

### 3.2 Recovery Techniques

| Technique | Tool | Effectiveness |
|---|---|---|
| Symbolic execution | angr, Triton, miasm | High — traces all state transitions |
| Trace-based recovery | Pin/DynamoRIO trace → reconstruct CFG | Medium — covers executed paths only |
| Pattern matching | Custom IDA/Ghidra script | Medium — works for known flatteners |
| D-810 (IDA plugin) | IDA Pro | High — specifically designed for CFF |

### 3.3 Symbolic Deflattening (angr approach)

```python
import angr, claripy

proj = angr.Project('./obfuscated')
cfg = proj.analyses.CFGFast()

# Find dispatcher block (highest in-degree basic block)
dispatcher = max(cfg.graph.nodes(), key=lambda n: cfg.graph.in_degree(n))

# For each case block, symbolically determine successor
for block in case_blocks:
    state = proj.factory.blank_state(addr=block.addr)
    # ... solve state variable to find real successor
```

---

## 4. MOVFUSCATOR

### 4.1 Concept

All computation reduced to `mov` instructions only (Turing-complete via memory-mapped computation tables). Created by Christopher Domas.

### 4.2 Identification

- Function contains only `mov` instructions (no add, sub, xor, jmp, call)
- Large lookup tables in data section
- Memory-mapped flag registers

### 4.3 Demovfuscation

| Approach | Description |
|---|---|
| demovfuscator (tool) | Static analysis, recovers original operations from mov patterns |
| Trace + taint analysis | Run with Pin/DynamoRIO, taint inputs, observe computation |
| Symbolic execution | Treat entire function as constraint system |

---

