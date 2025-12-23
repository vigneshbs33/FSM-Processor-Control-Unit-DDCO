# FSM-Based Processor Control Unit Project
## Digital Design and Computer Organization (DDCO)

### Authors
- **Vignesh B S** (1BI24IS187)
- **Rohit Maiya M** (1BI24IS131)

### Guide
- **Dr. Shilpa M**, Assistant Professor, ISE Department

---

## Project Structure

```
├── DDCO_Mini_Project_Report.md   # Academic report (5 pages)
├── README.md                      # This file
├── src/                           # Source Verilog files
│   ├── control_unit.v            # FSM-based Control Unit (main module)
│   ├── alu.v                     # Arithmetic Logic Unit
│   ├── register_file.v           # 4x8-bit Register File
│   ├── memory.v                  # 256x8-bit Memory
│   ├── program_counter.v         # Program Counter
│   ├── instruction_register.v    # Instruction Register
│   └── processor_top.v           # Top-level processor integration
└── testbench/                     # Testbench files
    ├── control_unit_tb.v         # Control Unit testbench
    └── processor_tb.v            # Full processor testbench
```

---

## Instruction Set

| Opcode | Mnemonic | Operation |
|--------|----------|-----------|
| 000 | ADD | Rd ← Rs + Rt |
| 001 | SUB | Rd ← Rs - Rt |
| 010 | AND | Rd ← Rs & Rt |
| 011 | OR | Rd ← Rs \| Rt |
| 100 | LOAD | Rd ← Mem[addr] |
| 101 | STORE | Mem[addr] ← Rs |
| 110 | BEQ | Branch if equal |
| 111 | HALT | Stop execution |

---

## FSM States

| State | Name | Description |
|-------|------|-------------|
| S0 | IDLE | Wait for start signal |
| S1 | FETCH | Fetch instruction from memory |
| S2 | DECODE | Decode opcode |
| S3 | EXECUTE_ALU | ALU operations |
| S4 | EXECUTE_MEM | Memory operations |
| S5 | EXECUTE_BR | Branch operations |
| S6 | WRITEBACK | Write results |
| S7 | HALT | Stop processor |

---

## Running Simulations

### Using Icarus Verilog (Open Source)

```bash
# Compile Control Unit testbench
iverilog -o cu_test src/control_unit.v testbench/control_unit_tb.v

# Run simulation
vvp cu_test

# View waveform
gtkwave control_unit_tb.vcd
```

### Using ModelSim

```bash
# Compile all files
vlog src/*.v testbench/*.v

# Run simulation
vsim -c processor_tb -do "run -all"
```

### Using Vivado

1. Create new RTL project
2. Add all .v files from src/ folder
3. Add testbench files
4. Run behavioral simulation

---

## Key Features

- **8-state Moore FSM** for control logic
- **8 instructions** (ALU, Memory, Branch, Halt)
- **8-bit datapath** with 4 general-purpose registers
- **256-byte memory** for instructions and data
- **Modular design** with separate components

---

## License

Academic project for educational purposes.
