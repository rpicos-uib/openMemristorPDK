// memristor_bit.v -- a digital twin of the Au/HfO2/Al memristor used
// as a 1-bit memory. No voltages or currents: only what a digital
// designer needs to know about it.
//
//   set   = 1 : a write pulse above +0.8 V -> the bit becomes 1
//   reset = 1 : a write pulse below -0.6 V -> the bit becomes 0
//   read  = 1 : a small 0.2 V read         -> q shows the bit
//
// A write only works if its pulse lasts at least T_SWITCH (15 ns, about
// what the ngspice simulation of the real model needs). When nothing
// happens the bit stays where it is: no power needed.
`timescale 1ns/1ps

module memristor_bit #(parameter T_SWITCH = 15) (
  input  wire set,
  input  wire reset,
  input  wire read,
  output wire q
);
  reg stored = 1'b0;   // x0 = 0: the memristor starts off

  // A SET pulse: wait T_SWITCH, then switch on if the pulse is still there.
  always @(posedge set) begin
    #(T_SWITCH);
    if (set) stored = 1'b1;
  end

  // A RESET pulse: the same, switching off.
  always @(posedge reset) begin
    #(T_SWITCH);
    if (reset) stored = 1'b0;
  end

  // While reading, q shows the bit; otherwise q is disconnected (z).
  assign q = read ? stored : 1'bz;
endmodule
