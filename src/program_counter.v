//==============================================================================
// Program Counter Module
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module program_counter (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire PCWrite,             // PC write enable
    input wire PCWriteCond,         // Conditional PC write (for branch)
    input wire zero_flag,           // Zero flag from ALU
    input wire [7:0] pc_next,       // Next PC value
    
    output reg [7:0] pc             // Current PC value
);

    //--------------------------------------------------------------------------
    // PC Update Logic
    // PC is updated when:
    // 1. PCWrite is high (unconditional update), OR
    // 2. PCWriteCond is high AND zero_flag is high (branch taken)
    //--------------------------------------------------------------------------
    wire pc_enable;
    assign pc_enable = PCWrite | (PCWriteCond & zero_flag);

    //--------------------------------------------------------------------------
    // Program Counter Register
    //--------------------------------------------------------------------------
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 8'b0;             // Reset PC to address 0
        end else if (pc_enable) begin
            pc <= pc_next;          // Update PC
        end
        // Else: PC holds its current value
    end

endmodule
