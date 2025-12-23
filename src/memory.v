//==============================================================================
// Memory Module (Instruction and Data Memory)
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module memory (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire MemRead,             // Memory read enable
    input wire MemWrite,            // Memory write enable
    input wire [7:0] address,       // Memory address (8-bit = 256 locations)
    input wire [7:0] write_data,    // Data to write
    
    output reg [7:0] read_data      // Data read from memory
);

    //--------------------------------------------------------------------------
    // Memory Array: 256 locations x 8 bits each
    //--------------------------------------------------------------------------
    reg [7:0] mem [0:255];
    
    //--------------------------------------------------------------------------
    // Integer for loops
    //--------------------------------------------------------------------------
    integer i;

    //--------------------------------------------------------------------------
    // Memory Initialization
    // Pre-load with sample program for testing
    //--------------------------------------------------------------------------
    initial begin
        // Initialize all memory to 0
        for (i = 0; i < 256; i = i + 1) begin
            mem[i] = 8'b0;
        end
        
        //----------------------------------------------------------------------
        // Sample Program: Test all instruction types
        // Instruction Format: [OPCODE(3)][Rd/Rs(2)][Rt/Imm(3)]
        //----------------------------------------------------------------------
        
        // Address 0: LOAD R0, [10]  - Load value from address 10 into R0
        // Opcode: 100, Rd: 00, Addr: 010 (address offset)
        mem[0] = 8'b100_00_010;     // LOAD R0, [2] -> loads from base+2
        
        // Address 1: LOAD R1, [11]  - Load value from address 11 into R1
        mem[1] = 8'b100_01_011;     // LOAD R1, [3]
        
        // Address 2: ADD R2, R0, R1 - R2 = R0 + R1
        // Opcode: 000, Rd: 10, Rs encoded in operation
        mem[2] = 8'b000_10_001;     // ADD R2 = R0 + R1
        
        // Address 3: SUB R3, R2, R0 - R3 = R2 - R0
        mem[3] = 8'b001_11_010;     // SUB R3 = R2 - R0
        
        // Address 4: AND R0, R1, R2 - R0 = R1 & R2
        mem[4] = 8'b010_00_010;     // AND R0 = R1 & R2
        
        // Address 5: OR R1, R0, R3  - R1 = R0 | R3
        mem[5] = 8'b011_01_011;     // OR R1 = R0 | R3
        
        // Address 6: STORE R2, [20] - Store R2 to address 20
        mem[6] = 8'b101_10_100;     // STORE R2 to [4] offset
        
        // Address 7: BEQ R0, R1, 2  - Branch if R0 == R1
        mem[7] = 8'b110_00_010;     // BEQ
        
        // Address 8: ADD R0, R0, R1 - R0 = R0 + R1 (skip if branched)
        mem[8] = 8'b000_00_001;     // ADD
        
        // Address 9: HALT
        mem[9] = 8'b111_00_000;     // HALT
        
        //----------------------------------------------------------------------
        // Data Section (starting at address 10)
        //----------------------------------------------------------------------
        mem[10] = 8'd15;            // Data: 15
        mem[11] = 8'd25;            // Data: 25
        mem[12] = 8'd5;             // Data: 5
        mem[13] = 8'd10;            // Data: 10
    end

    //--------------------------------------------------------------------------
    // Read Operation (Combinational with registered output)
    //--------------------------------------------------------------------------
    always @(*) begin
        if (MemRead) begin
            read_data = mem[address];
        end else begin
            read_data = 8'b0;
        end
    end

    //--------------------------------------------------------------------------
    // Write Operation (Sequential)
    //--------------------------------------------------------------------------
    always @(posedge clk) begin
        if (MemWrite) begin
            mem[address] <= write_data;
        end
    end

endmodule
