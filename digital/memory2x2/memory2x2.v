// memory2x2.v -- a 4-bit memory: the controller plus four memristor
// cells (the digital twin from ../memristor_bit/memristor_bit.v).
`timescale 1ns/1ps

module memory2x2 (
  input  wire       clk,
  input  wire       rst,
  input  wire       start,
  input  wire [1:0] op,
  input  wire [1:0] addr,
  output wire       data_out,
  output wire       busy
);
  wire [3:0] set, reset, read, q;

  mem_ctrl ctrl (.clk(clk), .rst(rst), .start(start), .op(op), .addr(addr),
                 .q(q), .set(set), .reset(reset), .read(read),
                 .data_out(data_out), .busy(busy));

  // Four memristors, one per address.
  memristor_bit cell0 (.set(set[0]), .reset(reset[0]), .read(read[0]), .q(q[0]));
  memristor_bit cell1 (.set(set[1]), .reset(reset[1]), .read(read[1]), .q(q[1]));
  memristor_bit cell2 (.set(set[2]), .reset(reset[2]), .read(read[2]), .q(q[2]));
  memristor_bit cell3 (.set(set[3]), .reset(reset[3]), .read(read[3]), .q(q[3]));
endmodule
