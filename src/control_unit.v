//==============================================================================
// Control Unit Module - FSM Based Implementation
// Project: Simple Processor Control Unit using Finite State Machines
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
// Guide: Dr. Shilpa M, ISE Department
// Course: Digital Design and Computer Organization (DDCO)
//==============================================================================

module control_unit (
    input wire clk,                 // System clock
    input wire reset,               // Asynchronous reset
    input wire start,               // Start execution signal
    input wire [2:0] opcode,        // Instruction opcode from IR
    input wire zero_flag,           // Zero flag from ALU (for branch)
    
    // Control Signals Output
    output reg PCWrite,             // Enable PC update
    output reg PCWriteCond,         // Conditional PC write (for branch)
    output reg IRWrite,             // Enable Instruction Register write
    output reg RegWrite,            // Enable Register File write
    output reg MemRead,             // Enable Memory read
    output reg MemWrite,            // Enable Memory write
    output reg ALUSrcA,             // ALU Source A select (0: PC, 1: RegA)
    output reg [1:0] ALUSrcB,       // ALU Source B select
    output reg [1:0] ALUOp,         // ALU Operation select
    output reg MemToReg,            // Register write source (0: ALU, 1: Memory)
    output reg IorD,                // Memory address source (0: PC, 1: ALU)
    output reg [2:0] current_state_out  // Current state output for debugging
);

    //--------------------------------------------------------------------------
    // State Encoding (One-hot or Binary encoding)
    //--------------------------------------------------------------------------
    parameter [2:0] IDLE        = 3'b000;   // S0: Initial state
    parameter [2:0] FETCH       = 3'b001;   // S1: Instruction Fetch
    parameter [2:0] DECODE      = 3'b010;   // S2: Instruction Decode
    parameter [2:0] EXECUTE_ALU = 3'b011;   // S3: ALU Execution
    parameter [2:0] EXECUTE_MEM = 3'b100;   // S4: Memory Access
    parameter [2:0] EXECUTE_BR  = 3'b101;   // S5: Branch Execution
    parameter [2:0] WRITEBACK   = 3'b110;   // S6: Write Back
    parameter [2:0] HALT_STATE  = 3'b111;   // S7: Halt

    //--------------------------------------------------------------------------
    // Opcode Definitions
    //--------------------------------------------------------------------------
    parameter [2:0] OP_ADD   = 3'b000;  // Addition
    parameter [2:0] OP_SUB   = 3'b001;  // Subtraction
    parameter [2:0] OP_AND   = 3'b010;  // Bitwise AND
    parameter [2:0] OP_OR    = 3'b011;  // Bitwise OR
    parameter [2:0] OP_LOAD  = 3'b100;  // Load from memory
    parameter [2:0] OP_STORE = 3'b101;  // Store to memory
    parameter [2:0] OP_BEQ   = 3'b110;  // Branch if equal
    parameter [2:0] OP_HALT  = 3'b111;  // Halt execution

    //--------------------------------------------------------------------------
    // State Registers
    //--------------------------------------------------------------------------
    reg [2:0] current_state, next_state;

    //--------------------------------------------------------------------------
    // State Output for Debugging
    //--------------------------------------------------------------------------
    always @(*) begin
        current_state_out = current_state;
    end

    //--------------------------------------------------------------------------
    // State Register (Sequential Logic)
    // Updates current state on positive clock edge or reset
    //--------------------------------------------------------------------------
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            current_state <= IDLE;
        end else begin
            current_state <= next_state;
        end
    end

    //--------------------------------------------------------------------------
    // Next State Logic (Combinational)
    // Determines the next state based on current state and inputs
    //--------------------------------------------------------------------------
    always @(*) begin
        // Default: stay in current state
        next_state = current_state;
        
        case (current_state)
            //------------------------------------------------------------------
            // IDLE State: Wait for start signal
            //------------------------------------------------------------------
            IDLE: begin
                if (start)
                    next_state = FETCH;
                else
                    next_state = IDLE;
            end
            
            //------------------------------------------------------------------
            // FETCH State: Always proceed to DECODE
            //------------------------------------------------------------------
            FETCH: begin
                next_state = DECODE;
            end
            
            //------------------------------------------------------------------
            // DECODE State: Determine execution path based on opcode
            //------------------------------------------------------------------
            DECODE: begin
                case (opcode)
                    OP_ADD, OP_SUB, OP_AND, OP_OR: begin
                        next_state = EXECUTE_ALU;
                    end
                    OP_LOAD, OP_STORE: begin
                        next_state = EXECUTE_MEM;
                    end
                    OP_BEQ: begin
                        next_state = EXECUTE_BR;
                    end
                    OP_HALT: begin
                        next_state = HALT_STATE;
                    end
                    default: begin
                        next_state = FETCH;
                    end
                endcase
            end
            
            //------------------------------------------------------------------
            // EXECUTE States: Proceed to WRITEBACK
            //------------------------------------------------------------------
            EXECUTE_ALU: begin
                next_state = WRITEBACK;
            end
            
            EXECUTE_MEM: begin
                next_state = WRITEBACK;
            end
            
            EXECUTE_BR: begin
                next_state = WRITEBACK;
            end
            
            //------------------------------------------------------------------
            // WRITEBACK State: Return to FETCH for next instruction
            //------------------------------------------------------------------
            WRITEBACK: begin
                next_state = FETCH;
            end
            
            //------------------------------------------------------------------
            // HALT State: Remain halted until reset
            //------------------------------------------------------------------
            HALT_STATE: begin
                if (reset)
                    next_state = IDLE;
                else
                    next_state = HALT_STATE;
            end
            
            //------------------------------------------------------------------
            // Default: Go to IDLE
            //------------------------------------------------------------------
            default: begin
                next_state = IDLE;
            end
        endcase
    end

    //--------------------------------------------------------------------------
    // Output Logic (Moore Machine - outputs depend only on current state)
    // Generates control signals based on current state
    //--------------------------------------------------------------------------
    always @(*) begin
        // Default: All control signals inactive
        PCWrite     = 1'b0;
        PCWriteCond = 1'b0;
        IRWrite     = 1'b0;
        RegWrite    = 1'b0;
        MemRead     = 1'b0;
        MemWrite    = 1'b0;
        ALUSrcA     = 1'b0;
        ALUSrcB     = 2'b00;
        ALUOp       = 2'b00;
        MemToReg    = 1'b0;
        IorD        = 1'b0;
        
        case (current_state)
            //------------------------------------------------------------------
            // IDLE: No active signals
            //------------------------------------------------------------------
            IDLE: begin
                // All signals remain at default (inactive)
            end
            
            //------------------------------------------------------------------
            // FETCH: Read instruction from memory
            // - Memory address from PC (IorD = 0)
            // - Read from memory (MemRead = 1)
            // - Load instruction register (IRWrite = 1)
            // - Increment PC (ALUSrcA = 0, ALUSrcB = 01, PCWrite = 1)
            //------------------------------------------------------------------
            FETCH: begin
                MemRead  = 1'b1;    // Read from memory
                IRWrite  = 1'b1;    // Write to IR
                IorD     = 1'b0;    // Address from PC
                ALUSrcA  = 1'b0;    // PC to ALU
                ALUSrcB  = 2'b01;   // Constant 1 to ALU
                ALUOp    = 2'b00;   // ADD operation
                PCWrite  = 1'b1;    // Update PC (PC = PC + 1)
            end
            
            //------------------------------------------------------------------
            // DECODE: Decode instruction and read registers
            // - Read register file (automatic)
            // - Compute branch target (ALUSrcA = 0, ALUSrcB = 11)
            //------------------------------------------------------------------
            DECODE: begin
                ALUSrcA  = 1'b0;    // PC for branch target calculation
                ALUSrcB  = 2'b11;   // Sign-extended immediate
                ALUOp    = 2'b00;   // ADD for branch target
            end
            
            //------------------------------------------------------------------
            // EXECUTE_ALU: Perform ALU operation
            // - Source A from register (ALUSrcA = 1)
            // - Source B from register (ALUSrcB = 00)
            // - ALU operation based on opcode
            //------------------------------------------------------------------
            EXECUTE_ALU: begin
                ALUSrcA  = 1'b1;    // Register A to ALU
                ALUSrcB  = 2'b00;   // Register B to ALU
                ALUOp    = 2'b10;   // R-type operation (function code decides)
            end
            
            //------------------------------------------------------------------
            // EXECUTE_MEM: Memory address calculation / access
            // - Calculate effective address
            // - Perform load or store
            //------------------------------------------------------------------
            EXECUTE_MEM: begin
                ALUSrcA  = 1'b1;    // Base address from register
                ALUSrcB  = 2'b10;   // Offset from immediate
                ALUOp    = 2'b00;   // ADD for address calculation
                IorD     = 1'b1;    // Address from ALU
                
                if (opcode == OP_LOAD) begin
                    MemRead = 1'b1;
                end else if (opcode == OP_STORE) begin
                    MemWrite = 1'b1;
                end
            end
            
            //------------------------------------------------------------------
            // EXECUTE_BR: Branch condition evaluation
            // - Compare registers (subtraction)
            // - Update PC if condition met
            //------------------------------------------------------------------
            EXECUTE_BR: begin
                ALUSrcA     = 1'b1;    // Register A
                ALUSrcB     = 2'b00;   // Register B
                ALUOp       = 2'b01;   // SUB for comparison
                PCWriteCond = 1'b1;    // Conditional PC write
            end
            
            //------------------------------------------------------------------
            // WRITEBACK: Write result to register file
            //------------------------------------------------------------------
            WRITEBACK: begin
                if (opcode == OP_LOAD) begin
                    RegWrite = 1'b1;
                    MemToReg = 1'b1;   // Data from memory
                end else if (opcode == OP_ADD || opcode == OP_SUB || 
                           opcode == OP_AND || opcode == OP_OR) begin
                    RegWrite = 1'b1;
                    MemToReg = 1'b0;   // Data from ALU
                end
                // STORE and BRANCH don't write to register
            end
            
            //------------------------------------------------------------------
            // HALT: All signals inactive, processor stopped
            //------------------------------------------------------------------
            HALT_STATE: begin
                // All signals remain at default (inactive)
            end
            
            default: begin
                // All signals remain at default
            end
        endcase
    end

endmodule
