For other original section numbers, use the [entry index](../SKILL.md#references).


# SKILL: VM & Bytecode Reverse Engineering — Expert Analysis Playbook

> **AI LOAD INSTRUCTION**: Expert techniques for reversing custom virtual machines and bytecode interpreters. Covers dispatcher identification, opcode mapping, custom ISA reconstruction, disassembler/decompiler writing, maze challenges, and real-world VM protector analysis. Base models often fail to recognize the fetch-decode-execute pattern or attempt to analyze VM bytecode as native code.

## 0. RELATED ROUTING

- [code-obfuscation-deobfuscation](../../code-obfuscation-deobfuscation/SKILL.md) when the VM is a commercial protector (VMProtect/Themida)
- [symbolic-execution-tools](../../symbolic-execution-tools/SKILL.md) when using angr to solve VM-based challenges
- [anti-debugging-techniques](../../anti-debugging-techniques/SKILL.md) when the VM includes anti-debug checks

### Quick identification

| Binary Pattern | Likely VM Type | Start With |
|---|---|---|
| `while(1) { switch(bytecode[pc]) }` | Switch-based dispatcher | Map each case to an operation |
| Indirect jump via table `jmp [table + opcode*8]` | Table-based dispatcher | Dump jump table, analyze handlers |
| Nested if-else chain on byte value | If-chain dispatcher | Same as switch, just different syntax |
| Stack push/pop dominant operations | Stack-based VM | Identify push, pop, arithmetic ops |
| `reg[X] = ...` array operations | Register-based VM | Map register indices to operations |
| 2D grid + direction input | Maze challenge | Extract grid, apply BFS/DFS |

---

## 1. CUSTOM VM IDENTIFICATION

### 1.1 Structural Indicators

```
VM Architecture Components:
┌─────────────────────────────────┐
│  Bytecode Program (data section)│
├─────────────────────────────────┤
│  Program Counter (pc/ip)        │
│  Register File / Stack          │
│  Memory / Data Area             │
├─────────────────────────────────┤
│  Dispatcher Loop                │
│  ├─ Fetch: opcode = code[pc]    │
│  ├─ Decode: lookup handler      │
│  └─ Execute: run handler        │
└─────────────────────────────────┘
```

### 1.2 IDA/Ghidra Signatures

**Switch dispatcher** (most common in CTF):
```c
while (running) {
    unsigned char op = bytecode[pc++];
    switch (op) {
        case 0x00: /* nop */       break;
        case 0x01: /* push imm */  stack[sp++] = bytecode[pc++]; break;
        case 0x02: /* add */       stack[sp-2] += stack[sp-1]; sp--; break;
        // ...
        case 0xFF: /* halt */      running = 0; break;
    }
}
```

**Table dispatcher** (more optimized):
```c
typedef void (*handler_t)(vm_ctx_t*);
handler_t handlers[256] = { handle_nop, handle_push, handle_add, ... };

while (running) {
    handlers[bytecode[pc++]](&ctx);
}
```

---

## 2. ANALYSIS METHODOLOGY

### Step 1: Find the Dispatcher

Look for:
- Large switch statement (many cases) in a loop
- Array of function pointers indexed by a byte from a data buffer
- Single function with high cyclomatic complexity
- Cross-references to a data buffer read byte-by-byte

### Step 2: Map Opcodes to Operations

For each case/handler, determine:

| Property | How to Identify |
|---|---|
| Opcode value | Case number or table index |
| Operation type | Register/stack modifications |
| Operand count | How many bytes consumed after opcode |
| Operand type | Immediate value, register index, or memory address |
| Side effects | Output, memory write, flag modification |

### Step 3: Extract Bytecode Program

```python
# Typical extraction from binary
import struct

with open('challenge', 'rb') as f:
    f.seek(bytecode_offset)
    bytecode = f.read(bytecode_length)

# Or from IDA:
# bytecode = idc.get_bytes(bytecode_addr, bytecode_len)
```

### Step 4: Write Custom Disassembler

```python
OPCODES = {
    0x00: ("nop",  0),    # (mnemonic, operand_bytes)
    0x01: ("push", 1),    # push immediate byte
    0x02: ("pop",  0),
    0x03: ("add",  0),
    0x04: ("sub",  0),
    0x05: ("xor",  0),
    0x06: ("cmp",  0),
    0x07: ("jmp",  2),    # jump to 16-bit address
    0x08: ("je",   2),
    0x09: ("jne",  2),
    0x0A: ("mov",  2),    # mov reg, imm
    0x0B: ("load", 1),    # load from memory[operand]
    0x0C: ("store",1),    # store to memory[operand]
    0x0D: ("print",0),
    0x0E: ("read", 0),    # read input
    0xFF: ("halt", 0),
}

def disassemble(bytecode):
    pc = 0
    while pc < len(bytecode):
        op = bytecode[pc]
        if op not in OPCODES:
            print(f"  {pc:04x}: UNKNOWN {op:#04x}")
            pc += 1
            continue

        mnemonic, operand_size = OPCODES[op]
        operands = bytecode[pc+1:pc+1+operand_size]
        operand_str = ' '.join(f'{b:#04x}' for b in operands)
        print(f"  {pc:04x}: {mnemonic:8s} {operand_str}")
        pc += 1 + operand_size

disassemble(bytecode)
```

### Step 5: Analyze Disassembled Program

With the custom disassembly, apply standard reverse engineering:
- Identify input reading (read opcode)
- Trace data flow from input to comparison
- Determine success/failure conditions
- Extract the check logic (often XOR/ADD transformations of input compared against constants)

---

