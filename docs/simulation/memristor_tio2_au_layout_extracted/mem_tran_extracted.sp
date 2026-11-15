Au/TiO2/Au memristor -- transient, driven through the real Magic-extracted layout
* memristor_tio2_au layout netlist (not a bare .model/instance line --
* BE/TE go through the real X0 device call Magic's own real device
* subcircuit recognition emitted). A real, confirmed ngspice behavior:
* its own implicit OSDI auto-load (matching an .osdi file in cwd to an
* unresolved .model name) only fires with no .subckt anywhere in the
* deck -- confirmed empirically, even for an unrelated, unused
* .subckt. The real, documented, explicit fix is `pre_osdi
* <file>.osdi` inside a leading .control block (loads the model
* before the netlist itself is parsed), the same real mechanism
* docs/simulation/memristor_tio2_au/.spiceinit's own `osdi
* memristor_tio2_au.osdi` line uses via a different real entry point.
.control
pre_osdi memristor_tio2_au.osdi
.endc

.model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0

.subckt memristor_tio2_au_prim BE TE
n1 BE TE mm
.ends

.include memristor_tio2_au_extracted.spice

* BE first, TE second here -- matches the real memristor_tio2_au.va
* module's own port order (BE, TE), and the real polarity the
* original hand-written testbench (../memristor_tio2_au/mem_tran.sp)
* drove: swapping this order flips I(BE,TE)'s own sign, and with it
* the sign of the internal state integrator -- a real, physically
* meaningful difference, not a formatting nicety (found by comparing
* against that original testbench's own real, already-verified
* result and seeing a real, non-trivial divergence until this was
* fixed).
X1 te 0 memristor_tio2_au
vte te 0 dc 0 sin(0 1.0 0.6)
.tran 300u 3.34
.control
run
wrdata memristor_extracted_tran.csv v(te) i(vte)
.endc
.end
