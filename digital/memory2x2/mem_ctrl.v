// mem_ctrl.v -- a tiny controller for a 4-bit memristor memory.
// It turns "write a 1 into cell 2" or "read cell 3" into the right
// pulses, long enough for a memristor to switch:
//   write: PULSE clock cycles of set or reset on one cell,
//   read:  READ  clock cycles of read on one cell, then it keeps the bit.
// With a 10 ns clock, PULSE = 8 gives an 80 ns pulse, like the xschem
// testbenches. This file is real logic: Yosys turns it into gates.
// (No `timescale here: it has no delays, only clock ticks.)

module mem_ctrl #(parameter PULSE = 8, parameter READ = 4) (
  input  wire       clk,
  input  wire       rst,       // 1: stop and start over
  input  wire       start,     // 1 for one clock: begin an operation
  input  wire [1:0] op,        // 0 = read, 1 = write 1, 2 = write 0
  input  wire [1:0] addr,      // which cell: 0, 1, 2 or 3
  input  wire [3:0] q,         // what the cells show while being read
  output wire [3:0] set,       // write-1 pulse, one wire per cell
  output wire [3:0] reset,     // write-0 pulse, one wire per cell
  output wire [3:0] read,      // read pulse, one wire per cell
  output reg        data_out,  // the last bit read
  output reg        busy       // 1 while an operation is going on
);
  reg [1:0] cur_op;
  reg [1:0] cur_addr;
  reg [3:0] count;

  // Only the chosen cell gets a pulse: 1 shifted to its position.
  wire [3:0] chosen = 4'b0001 << cur_addr;

  assign set   = (busy && cur_op == 2'd1) ? chosen : 4'b0000;
  assign reset = (busy && cur_op == 2'd2) ? chosen : 4'b0000;
  assign read  = (busy && cur_op == 2'd0) ? chosen : 4'b0000;

  always @(posedge clk) begin
    if (rst) begin
      busy     <= 1'b0;
      count    <= 4'd0;
      data_out <= 1'b0;
      cur_op   <= 2'd0;
      cur_addr <= 2'd0;
    end else if (!busy) begin
      if (start) begin              // remember what to do, then start
        busy     <= 1'b1;
        cur_op   <= op;
        cur_addr <= addr;
        count    <= 4'd0;
      end
    end else begin
      count <= count + 4'd1;
      if (cur_op == 2'd0 && count == READ - 1) begin
        data_out <= q[cur_addr];    // the end of a read: keep the bit
        busy     <= 1'b0;
      end else if (cur_op != 2'd0 && count == PULSE - 1) begin
        busy     <= 1'b0;           // the end of a write
      end
    end
  end
endmodule
