//==============================================================================
// Register File Module
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module register_file (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire RegWrite,            // Write enable signal from Control Unit
    
    input wire [1:0] read_reg1,     // Read register 1 address
    input wire [1:0] read_reg2,     // Read register 2 address
    input wire [1:0] write_reg,     // Write register address
    input wire [7:0] write_data,    // Data to write
    
    output wire [7:0] read_data1,   // Data from register 1
    output wire [7:0] read_data2    // Data from register 2
);

    //--------------------------------------------------------------------------
    // Register Array: 4 registers x 8 bits each
    // R0, R1, R2, R3
    //--------------------------------------------------------------------------
    reg [7:0] registers [0:3];
    
    //--------------------------------------------------------------------------
    // Integer for reset loop
    //--------------------------------------------------------------------------
    integer i;

    //--------------------------------------------------------------------------
    // Read Operation (Combinational - Asynchronous Read)
    // Data is available immediately based on address
    //--------------------------------------------------------------------------
    assign read_data1 = registers[read_reg1];
    assign read_data2 = registers[read_reg2];

    //--------------------------------------------------------------------------
    // Write Operation (Sequential - Synchronous Write)
    // Data is written on positive clock edge when RegWrite is high
    //--------------------------------------------------------------------------
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset all registers to 0
            for (i = 0; i < 4; i = i + 1) begin
                registers[i] <= 8'b0;
            end
        end else if (RegWrite) begin
            // Write data to specified register
            registers[write_reg] <= write_data;
        end
    end

endmodule
