// memristor_bit_tb.v -- the same test as memristor_hfo2_al_bit_tb in
// xschem: read, write 1, read, write 0, read, 100 ns each. Then one
// more write 1 that is too short (5 ns), and a last read.
`timescale 1ns/1ps

module memristor_bit_tb;
  reg set = 0, reset = 0, read = 0;
  wire q;

  memristor_bit m1 (.set(set), .reset(reset), .read(read), .q(q));

  // Read for 80 ns and print what q shows halfway through.
  task read_bit(input [8*24:1] when);
    begin
      read = 1; #40;
      $display("%0d ns: read %0s -> q = %b", $time, when, q);
      #40 read = 0; #20;
    end
  endtask

  initial begin
    $dumpfile("memristor_bit_tb.vcd");    // the waveforms, for GTKWave
    $dumpvars(0, memristor_bit_tb);
    read_bit("before any write");
    set = 1;   #80 set = 0;   #20;          // write 1 (80 ns pulse)
    read_bit("after write 1");
    reset = 1; #80 reset = 0; #20;          // write 0 (80 ns pulse)
    read_bit("after write 0");
    set = 1;   #5  set = 0;   #95;          // write 1, but only 5 ns
    read_bit("after a 5 ns write 1");
    $finish;
  end
endmodule
