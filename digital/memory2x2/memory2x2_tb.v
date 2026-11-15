// memory2x2_tb.v -- write the pattern 1 0 0 1 into the 4-bit memory,
// read all four cells back, then overwrite cell 0 with a 0.
`timescale 1ns/1ps

module memory2x2_tb;
  reg clk = 0, rst = 1, start = 0;
  reg [1:0] op = 0, addr = 0;
  wire data_out, busy;

  memory2x2 mem (.clk(clk), .rst(rst), .start(start), .op(op), .addr(addr),
                 .data_out(data_out), .busy(busy));

  always #5 clk = ~clk;              // a 10 ns clock (100 MHz)

  // Ask for one operation and wait until the controller is done.
  task do_op(input [1:0] o, input [1:0] a);
    begin
      @(negedge clk); op = o; addr = a; start = 1;
      @(negedge clk); start = 0;
      wait (!busy); @(negedge clk);
    end
  endtask

  task write_bit(input [1:0] a, input v);
    begin
      do_op(v ? 2'd1 : 2'd2, a);
      $display("%0d ns: wrote %b into cell %0d", $time, v, a);
    end
  endtask

  task read_bit(input [1:0] a);
    begin
      do_op(2'd0, a);
      $display("%0d ns: read cell %0d -> %b", $time, a, data_out);
    end
  endtask

  initial begin
    $dumpfile("memory2x2_tb.vcd");
    $dumpvars(0, memory2x2_tb);
    #20 rst = 0;
    write_bit(0, 1);                 // the pattern 1 0 0 1
    write_bit(3, 1);
    read_bit(0); read_bit(1); read_bit(2); read_bit(3);
    write_bit(0, 0);                 // change cell 0 back to 0
    read_bit(0);
    $finish;
  end
endmodule
