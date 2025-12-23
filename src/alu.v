//==============================================================================
// ALU (Arithmetic Logic Unit) Module
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module alu (
    input wire [7:0] A,             // First operand
    input wire [7:0] B,             // Second operand
    input wire [1:0] ALUOp,         // ALU operation control from Control Unit
    input wire [2:0] funct,         // Function code for R-type instructions
    
    output reg [7:0] result,        // ALU result
    output wire zero,               // Zero flag (result == 0)
    output wire negative,           // Negative flag (result[7] == 1)
    output wire carry               // Carry flag
);

    //--------------------------------------------------------------------------
    // ALU Operation Codes
    //--------------------------------------------------------------------------
    parameter [1:0] ALUOP_ADD  = 2'b00;  // Addition (for PC increment, address calc)
    parameter [1:0] ALUOP_SUB  = 2'b01;  // Subtraction (for comparison)
    parameter [1:0] ALUOP_FUNC = 2'b10;  // Function-based (R-type instructions)
    parameter [1:0] ALUOP_PASS = 2'b11;  // Pass through A

    //--------------------------------------------------------------------------
    // Function Codes (from opcode lower bits for R-type)
    //--------------------------------------------------------------------------
    parameter [2:0] FUNC_ADD = 3'b000;  // Addition
    parameter [2:0] FUNC_SUB = 3'b001;  // Subtraction
    parameter [2:0] FUNC_AND = 3'b010;  // Bitwise AND
    parameter [2:0] FUNC_OR  = 3'b011;  // Bitwise OR
    parameter [2:0] FUNC_XOR = 3'b100;  // Bitwise XOR
    parameter [2:0] FUNC_SLT = 3'b101;  // Set Less Than
    parameter [2:0] FUNC_SLL = 3'b110;  // Shift Left Logical
    parameter [2:0] FUNC_SRL = 3'b111;  // Shift Right Logical

    //--------------------------------------------------------------------------
    // Internal Signals
    //--------------------------------------------------------------------------
    reg [8:0] temp_result;  // 9-bit for carry detection

    //--------------------------------------------------------------------------
    // ALU Operation Logic
    //--------------------------------------------------------------------------
    always @(*) begin
        temp_result = 9'b0;
        result = 8'b0;
        
        case (ALUOp)
            //------------------------------------------------------------------
            // ADD: Used for PC increment and address calculation
            //------------------------------------------------------------------
            ALUOP_ADD: begin
                temp_result = {1'b0, A} + {1'b0, B};
                result = temp_result[7:0];
            end
            
            //------------------------------------------------------------------
            // SUB: Used for branch comparison
            //------------------------------------------------------------------
            ALUOP_SUB: begin
                temp_result = {1'b0, A} - {1'b0, B};
                result = temp_result[7:0];
            end
            
            //------------------------------------------------------------------
            // FUNC: R-type instructions - operation based on function code
            //------------------------------------------------------------------
            ALUOP_FUNC: begin
                case (funct)
                    FUNC_ADD: begin
                        temp_result = {1'b0, A} + {1'b0, B};
                        result = temp_result[7:0];
                    end
                    
                    FUNC_SUB: begin
                        temp_result = {1'b0, A} - {1'b0, B};
                        result = temp_result[7:0];
                    end
                    
                    FUNC_AND: begin
                        result = A & B;
                    end
                    
                    FUNC_OR: begin
                        result = A | B;
                    end
                    
                    FUNC_XOR: begin
                        result = A ^ B;
                    end
                    
                    FUNC_SLT: begin
                        // Set to 1 if A < B (signed comparison)
                        result = ($signed(A) < $signed(B)) ? 8'b1 : 8'b0;
                    end
                    
                    FUNC_SLL: begin
                        // Shift left by B[2:0] positions
                        result = A << B[2:0];
                    end
                    
                    FUNC_SRL: begin
                        // Shift right by B[2:0] positions
                        result = A >> B[2:0];
                    end
                    
                    default: begin
                        result = A;  // Pass through
                    end
                endcase
            end
            
            //------------------------------------------------------------------
            // PASS: Pass through operand A
            //------------------------------------------------------------------
            ALUOP_PASS: begin
                result = A;
            end
            
            default: begin
                result = 8'b0;
            end
        endcase
    end

    //--------------------------------------------------------------------------
    // Flag Generation
    //--------------------------------------------------------------------------
    assign zero     = (result == 8'b0);           // Zero when result is 0
    assign negative = result[7];                   // Sign bit
    assign carry    = temp_result[8];             // Carry out

endmodule
