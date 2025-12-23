//==============================================================================
// Processor Top-Level Testbench
// Authors: Vignesh B S (1BI24IS187), Rohit Maiya M (1BI24IS131)
//==============================================================================

`timescale 1ns/1ps

module processor_tb;
    reg clk, reset, start;
    wire [7:0] pc_out, ir_out, alu_result_out;
    wire [2:0] state_out;
    wire halt;

    processor_top DUT (
        .clk(clk), .reset(reset), .start(start),
        .pc_out(pc_out), .ir_out(ir_out),
        .state_out(state_out), .alu_result_out(alu_result_out),
        .halt(halt)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        $display("=== Processor Testbench ===");
        $display("Testing instruction execution...\n");
        
        reset = 1; start = 0;
        #20 reset = 0;
        #10 start = 1;
        
        // Run until halt or 500ns
        repeat(50) begin
            #10;
            $display("PC=%d IR=%b State=%d ALU=%d Halt=%b",
                     pc_out, ir_out, state_out, alu_result_out, halt);
            if (halt) begin
                $display("\n=== Processor HALTED ===");
                #20 $finish;
            end
        end
        
        $display("Simulation timeout");
        $finish;
    end

    initial begin
        $dumpfile("processor_tb.vcd");
        $dumpvars(0, processor_tb);
    end
endmodule
