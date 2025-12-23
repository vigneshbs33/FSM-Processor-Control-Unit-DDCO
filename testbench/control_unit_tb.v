//==============================================================================
// Control Unit Testbench
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
//==============================================================================

`timescale 1ns/1ps

module control_unit_tb;
    reg clk, reset, start;
    reg [2:0] opcode;
    reg zero_flag;
    
    wire PCWrite, PCWriteCond, IRWrite, RegWrite, MemRead, MemWrite;
    wire ALUSrcA, MemToReg, IorD;
    wire [1:0] ALUSrcB, ALUOp;
    wire [2:0] current_state;

    control_unit DUT (
        .clk(clk), .reset(reset), .start(start),
        .opcode(opcode), .zero_flag(zero_flag),
        .PCWrite(PCWrite), .PCWriteCond(PCWriteCond),
        .IRWrite(IRWrite), .RegWrite(RegWrite),
        .MemRead(MemRead), .MemWrite(MemWrite),
        .ALUSrcA(ALUSrcA), .ALUSrcB(ALUSrcB),
        .ALUOp(ALUOp), .MemToReg(MemToReg),
        .IorD(IorD), .current_state_out(current_state)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        $display("=== Control Unit FSM Testbench ===");
        reset = 1; start = 0; opcode = 0; zero_flag = 0;
        #20 reset = 0;
        
        // Test ADD
        start = 1; opcode = 3'b000;
        repeat(5) #10 $display("State=%d Op=ADD", current_state);
        
        // Test LOAD
        opcode = 3'b100;
        repeat(4) #10 $display("State=%d Op=LOAD MemRead=%b", current_state, MemRead);
        
        // Test STORE
        opcode = 3'b101;
        repeat(4) #10 $display("State=%d Op=STORE MemWrite=%b", current_state, MemWrite);
        
        // Test HALT
        opcode = 3'b111;
        repeat(4) #10 $display("State=%d Op=HALT", current_state);
        
        $display("=== All Tests Completed ===");
        #20 $finish;
    end

    initial begin
        $dumpfile("control_unit_tb.vcd");
        $dumpvars(0, control_unit_tb);
    end
endmodule
