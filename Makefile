# Makefile for FSM Processor Control Unit Project
# Using Icarus Verilog

# Directories
SRC_DIR = src
TB_DIR = testbench

# Source files
SRCS = $(SRC_DIR)/control_unit.v \
       $(SRC_DIR)/alu.v \
       $(SRC_DIR)/register_file.v \
       $(SRC_DIR)/memory.v \
       $(SRC_DIR)/program_counter.v \
       $(SRC_DIR)/instruction_register.v \
       $(SRC_DIR)/processor_top.v

# Testbenches
CU_TB = $(TB_DIR)/control_unit_tb.v
PROC_TB = $(TB_DIR)/processor_tb.v

# Output files
CU_OUT = cu_sim
PROC_OUT = proc_sim

# Default target
all: control_unit processor

# Compile and run Control Unit testbench
control_unit:
	iverilog -o $(CU_OUT) $(SRC_DIR)/control_unit.v $(CU_TB)
	vvp $(CU_OUT)

# Compile and run full Processor testbench
processor:
	iverilog -o $(PROC_OUT) $(SRCS) $(PROC_TB)
	vvp $(PROC_OUT)

# View waveforms
wave_cu:
	gtkwave control_unit_tb.vcd &

wave_proc:
	gtkwave processor_tb.vcd &

# Clean generated files
clean:
	rm -f $(CU_OUT) $(PROC_OUT) *.vcd

.PHONY: all control_unit processor wave_cu wave_proc clean
