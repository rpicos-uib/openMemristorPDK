# Makefile -- the commands of the digital flow for the 4-bit memory.
#
#   make sim    simulate the controller + 4 memristor twins (Icarus Verilog)
#   make synth  turn the controller into IHP SG13G2 logic gates (Yosys)
#   make gates  synthesize, then simulate again with the gates
#   make clean  delete everything the other commands made
PDK_ROOT ?= /foss/pdks
STDCELL  := $(PDK_ROOT)/ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog
TWIN     := ../memristor_bit/memristor_bit.v

sim:
	iverilog -o memory2x2_tb mem_ctrl.v memory2x2.v $(TWIN) memory2x2_tb.v
	vvp -n memory2x2_tb

synth:
	yosys -q -s synth.ys
	@grep -E "cells$$|sg13g2_|Chip area" mem_ctrl_stats.txt

# IHP's gate models carry timing details Icarus Verilog can't use; it
# prints a "sorry:" line for each one. They are harmless, so hidden.
gates: synth
	@iverilog -o gates_tb mem_ctrl_gates.v memory2x2.v $(TWIN) memory2x2_tb.v \
	  $(STDCELL)/sg13g2_stdcell.v $(STDCELL)/sg13g2_udp.v 2>&1 | grep -v "sorry:" || true
	vvp -n gates_tb

clean:
	rm -f memory2x2_tb gates_tb *.vcd mem_ctrl_gates.v mem_ctrl_stats.txt

.PHONY: sim synth gates clean
