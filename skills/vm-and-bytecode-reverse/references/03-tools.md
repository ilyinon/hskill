# vm-and-bytecode-reverse technical reference

For other original section numbers, use the [entry index](../SKILL.md#references).

## 6. TOOLS

| Tool | Purpose | Usage |
|---|---|---|
| IDA Pro | Identify dispatcher, reverse handlers | F5 decompile, xref analysis |
| Ghidra | Free alternative with Sleigh processor modules | Write custom processor for VM ISA |
| angr | Symbolic execution through VM | Treat entire VM as constraint system |
| Pin / DynamoRIO | Dynamic instrumentation for tracing | Record opcode handler execution sequence |
| REVEN | Full-system trace recording | Replay and analyze VM execution |
| Unicorn | Emulate VM execution | Fast handler emulation |
| Miasm | IR-based analysis | Lift VM handlers to IR for analysis |
| Custom Python | Write disassembler/decompiler | Per-challenge custom tooling |

### Ghidra Sleigh Processor Module

For recurring VM architectures, write a Sleigh processor specification:

```
define space ram      type=ram_space      size=2  default;
define space register type=register_space  size=1;

define register offset=0 size=1 [ R0 R1 R2 R3 FLAGS PC SP ];

define token opcode(8)
    op = (0,7)
;

:NOP    is op=0x00 { }
:PUSH   imm is op=0x01; imm { SP = SP - 1; *[ram]:1 SP = imm; }
:POP    is op=0x02 { SP = SP + 1; }
:ADD    is op=0x03 { local a = *[ram]:1 (SP+1); *[ram]:1 (SP+1) = a + *[ram]:1 SP; SP = SP + 1; }
```

---

## 7. DECISION TREE

```
Binary contains custom bytecode interpreter?
│
├─ Can you identify the dispatcher?
│  ├─ Yes (switch/table/if-chain)
│  │  ├─ Few opcodes (< 20) → Simple CTF VM
│  │  │  ├─ Stack-based → map push/pop/arithmetic ops
│  │  │  ├─ Register-based → map mov/add/cmp ops
│  │  │  └─ Write disassembler → analyze program → solve
│  │  │
│  │  └─ Many opcodes (50+) → Commercial protector
│  │     ├─ Known protector → use specific deprotection tools
│  │     └─ Custom → trace execution, pattern-match handlers
│  │
│  └─ No clear dispatcher
│     ├─ All-mov instructions → movfuscator
│     ├─ Encrypted bytecode → find decryption, dump after decode
│     └─ Split/distributed handlers → trace execution to find them
│
├─ Is it a maze challenge?
│  ├─ Extract grid from data section
│  ├─ Identify direction encoding
│  ├─ BFS/DFS to find shortest path
│  └─ Convert path to expected input format
│
├─ Is there input validation in VM?
│  ├─ Small input space → brute-force via Unicorn emulation
│  ├─ Known format → constrained angr solve
│  └─ Complex check → write disassembler, analyze check logic
│
└─ Multiple VM layers (VM in VM)?
   ├─ Analyze outer VM first
   ├─ Extract inner bytecode
   ├─ Repeat analysis for inner VM
   └─ Consider: symbolic execution may handle nested VMs directly
```

---

## 8. CTF SOLVING WORKFLOW

```
1. Run the binary — understand I/O behavior
   └─ What input does it expect? What output on success/failure?

2. Open in IDA/Ghidra — find the main loop
   └─ Look for while/for loop with switch or indirect jump

3. Identify VM components:
   ├─ Bytecode location (where is the program data?)
   ├─ PC/IP variable (how is current position tracked?)
   ├─ Registers/stack (where is VM state stored?)
   └─ I/O handlers (which opcodes read input / write output?)

4. Map all opcodes (create the ISA specification)
   └─ For each case/handler: opcode number, operation, operands

5. Write disassembler in Python
   └─ Output readable assembly for the bytecode

6. Analyze the disassembled program:
   ├─ Find input reading
   ├─ Trace transformations applied to input
   ├─ Find comparison against expected values
   └─ Reverse the transformation to find valid input

7. Solve:
   ├─ If simple transforms (XOR, ADD) → reverse manually
   ├─ If complex → feed to Z3 as constraints
   └─ If maze → extract grid, run pathfinding
```
