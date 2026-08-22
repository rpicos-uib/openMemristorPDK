4x4 Au/TiO2/Au memristor crossbar -- real write-then-read, driven through the real, live xschem-netlisted schematic
* The exact same real testbench as crossbar_write_read_extracted.sp --
* same real PWL drive, same real timing, same real Vw/Vr -- with only
* one real difference: crossbar4x4_tio2_au here resolves to the real,
* behavioral schematic netlist (gen_schematic_netlist.py's own real
* output, 16 real "n... mm" device lines straight from real, live
* xschem) instead of the real, patched Magic-extracted layout netlist.
* A real, direct check that both real views of this cell -- schematic
* and extracted -- don't just match topologically (Step 9's own real
* LVS) but simulate identically too.
.control
pre_osdi memristor_tio2_au.osdi
.endc

.model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0.3

.include crossbar4x4_tio2_au_schematic.spice

X0 be1 be2 be3 be4 te1 te2 te3 te4 crossbar4x4_tio2_au

vbe1 be1 0 PWL(0 1.0  0.9 1.0  0.900001 0.05  1.4 0.05  1.400001 0.0  2.9 0.0)
vbe2 be2 0 PWL(0 0.5  0.9 0.5  0.900001 0.0   1.4 0.0   1.400001 0.05  1.9 0.05  1.900001 0.0  2.9 0.0)
vbe3 be3 0 PWL(0 0.5  0.9 0.5  0.900001 0.0   1.9 0.0   1.900001 0.05  2.4 0.05  2.400001 0.0  2.9 0.0)
vbe4 be4 0 PWL(0 0.5  0.9 0.5  0.900001 0.0   2.4 0.0   2.400001 0.05  2.9 0.05)
vte1 te1 0 dc 0
vte2 te2 0 PWL(0 0.5  0.9 0.5  0.900001 0.0  2.9 0.0)
vte3 te3 0 PWL(0 0.5  0.9 0.5  0.900001 0.0  2.9 0.0)
vte4 te4 0 PWL(0 0.5  0.9 0.5  0.900001 0.0  2.9 0.0)

.tran 0.2m 2.9

.control
run
wrdata crossbar4x4_write_read_schematic.csv v(be1) v(be2) v(be3) v(be4) v(te1) v(te2) v(te3) v(te4) i(vte1) i(vte2) i(vte3) i(vte4)
.endc
.end
