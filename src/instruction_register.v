//==============================================================================
// Instruction Register Module
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module instruction_register (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire IRWrite,             // IR write enable from Control Unit
    input wire [7:0] instruction,   // Instruction from memory
    
    output reg [7:0] IR,            // Full instruction
    output wire [2:0] opcode,       // Opcode field (bits 7-5)
    output wire [1:0] rs,           // Source register / Destination (bits 4-3)
    output wire [2:0] rt_imm        // Second register / Immediate (bits 2-0)
);

    //--------------------------------------------------------------------------
    // Instruction Register
    // Stores the current instruction being executed
    //--------------------------------------------------------------------------
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            IR <= 8'b0;
        end else if (IRWrite) begin
            IR <= instruction;
        end
        // Else: IR holds its current value
    end

    //--------------------------------------------------------------------------
    // Instruction Field Extraction
    // Instruction Format: [OPCODE(3)][RS/RD(2)][RT/IMM(3)]
    //--------------------------------------------------------------------------
    assign opcode  = IR[7:5];       // Operation code
    assign rs      = IR[4:3];       // Source/Destination register
    assign rt_imm  = IR[2:0];       // Second register or Immediate value

endmodule
