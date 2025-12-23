//==============================================================================
// Top-Level Processor Module
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module processor_top (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire start,               // Start execution
    
    // Debug/Observation ports
    output wire [7:0] pc_out,       // Current PC value
    output wire [7:0] ir_out,       // Current instruction
    output wire [2:0] state_out,    // Current FSM state
    output wire [7:0] alu_result_out, // ALU result
    output wire halt                // Processor halted
);

    //--------------------------------------------------------------------------
    // Internal Wires - Control Signals
    //--------------------------------------------------------------------------
    wire PCWrite, PCWriteCond, IRWrite;
    wire RegWrite, MemRead, MemWrite;
    wire ALUSrcA;
    wire [1:0] ALUSrcB;
    wire [1:0] ALUOp;
    wire MemToReg, IorD;
    
    //--------------------------------------------------------------------------
    // Internal Wires - Data Signals
    //--------------------------------------------------------------------------
    wire [7:0] pc, pc_next;
    wire [7:0] instruction, ir;
    wire [2:0] opcode;
    wire [1:0] rs;
    wire [2:0] rt_imm;
    
    wire [7:0] read_data1, read_data2;
    wire [7:0] alu_a, alu_b;
    wire [7:0] alu_result;
    wire zero_flag, negative_flag, carry_flag;
    
    wire [7:0] mem_address;
    wire [7:0] mem_read_data;
    wire [7:0] write_back_data;
    
    //--------------------------------------------------------------------------
    // Output Assignments
    //--------------------------------------------------------------------------
    assign pc_out = pc;
    assign ir_out = ir;
    assign alu_result_out = alu_result;
    assign halt = (state_out == 3'b111);  // HALT state
    
    //--------------------------------------------------------------------------
    // Control Unit Instance
    //--------------------------------------------------------------------------
    control_unit CU (
        .clk(clk),
        .reset(reset),
        .start(start),
        .opcode(opcode),
        .zero_flag(zero_flag),
        
        .PCWrite(PCWrite),
        .PCWriteCond(PCWriteCond),
        .IRWrite(IRWrite),
        .RegWrite(RegWrite),
        .MemRead(MemRead),
        .MemWrite(MemWrite),
        .ALUSrcA(ALUSrcA),
        .ALUSrcB(ALUSrcB),
        .ALUOp(ALUOp),
        .MemToReg(MemToReg),
        .IorD(IorD),
        .current_state_out(state_out)
    );
    
    //--------------------------------------------------------------------------
    // Program Counter Instance
    //--------------------------------------------------------------------------
    program_counter PC_unit (
        .clk(clk),
        .reset(reset),
        .PCWrite(PCWrite),
        .PCWriteCond(PCWriteCond),
        .zero_flag(zero_flag),
        .pc_next(alu_result),       // Next PC from ALU
        .pc(pc)
    );
    
    //--------------------------------------------------------------------------
    // Memory Instance
    //--------------------------------------------------------------------------
    // Memory address selection: PC (instruction fetch) or ALU result (data access)
    assign mem_address = IorD ? alu_result : pc;
    
    memory MEM (
        .clk(clk),
        .reset(reset),
        .MemRead(MemRead),
        .MemWrite(MemWrite),
        .address(mem_address),
        .write_data(read_data2),    // Store data from register
        .read_data(mem_read_data)
    );
    
    //--------------------------------------------------------------------------
    // Instruction Register Instance
    //--------------------------------------------------------------------------
    instruction_register IR_unit (
        .clk(clk),
        .reset(reset),
        .IRWrite(IRWrite),
        .instruction(mem_read_data),
        .IR(ir),
        .opcode(opcode),
        .rs(rs),
        .rt_imm(rt_imm)
    );
    
    //--------------------------------------------------------------------------
    // Register File Instance
    //--------------------------------------------------------------------------
    // Write-back data selection: Memory data or ALU result
    assign write_back_data = MemToReg ? mem_read_data : alu_result;
    
    register_file REG_FILE (
        .clk(clk),
        .reset(reset),
        .RegWrite(RegWrite),
        .read_reg1(rs),
        .read_reg2(rt_imm[1:0]),    // Lower 2 bits of rt_imm field
        .write_reg(rs),              // Destination is same as source field
        .write_data(write_back_data),
        .read_data1(read_data1),
        .read_data2(read_data2)
    );
    
    //--------------------------------------------------------------------------
    // ALU Source Multiplexers
    //--------------------------------------------------------------------------
    // ALU Source A: PC (0) or Register A (1)
    assign alu_a = ALUSrcA ? read_data1 : pc;
    
    // ALU Source B: Register B (00), Constant 1 (01), Immediate (10), Sign-ext (11)
    assign alu_b = (ALUSrcB == 2'b00) ? read_data2 :
                   (ALUSrcB == 2'b01) ? 8'd1 :
                   (ALUSrcB == 2'b10) ? {5'b0, rt_imm} :
                   {{5{rt_imm[2]}}, rt_imm};  // Sign-extended immediate
    
    //--------------------------------------------------------------------------
    // ALU Instance
    //--------------------------------------------------------------------------
    alu ALU_unit (
        .A(alu_a),
        .B(alu_b),
        .ALUOp(ALUOp),
        .funct(opcode),             // Use opcode for function selection
        .result(alu_result),
        .zero(zero_flag),
        .negative(negative_flag),
        .carry(carry_flag)
    );

endmodule
