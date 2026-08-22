4x4 Au/TiO2/Au memristor crossbar -- real write-then-read, driven through the real, patched Magic-extracted layout netlist
* Same real V/2 row/column biasing as the 2x2 deck (selected row =
* Vw, selected column = 0, every other row/column = Vw/2), scaled up
* to 4 rows/4 columns: writes just cell (1,1). Cells (1,2)/(1,3)/(1,4)
* (same row) and (2,1)/(3,1)/(4,1) (same column) all sit at the real
* Vw/2 half-select voltage during that one write -- the real
* algebraic symmetry already confirmed for 2x2 holds for any real
* NxN array, since a same-row cell sees (Vw - Vw/2) and a same-column
* cell sees just Vw/2, equal for any N. The remaining 9 real cells
* (any row/column other than 1) see 0V throughout -- real, untouched
* controls. Reads then drive one real row at a time at a small Vr
* (every TE column held at 0, all 4 real ammeters live), reading all
* 4 of that row's real cells at once -- 4 real read phases instead of
* 2x2's 2, same real per-phase duration and Vr.
.control
pre_osdi memristor_tio2_au.osdi
.endc

.model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0.3

.subckt memristor_tio2_au_prim BE TE
n1 BE TE mm
.ends

.include crossbar4x4_tio2_au_extracted.spice

X0 be1 be2 be3 be4 te1 te2 te3 te4 crossbar4x4_tio2_au

* --- real, discrete PWL row/column drive -------------------------------
* t=[0,0.9): WRITE (1,1) only -- be1=1.0 te1=0.0 (full Vw), be2=be3=
*   be4=te2=te3=te4=0.5 (real V/2 unselect).
* t=[0.9,1.4): READ row 1 -- be1=0.05 (Vr), everything else 0.
* t=[1.4,1.9): READ row 2 -- be2=0.05, everything else 0.
* t=[1.9,2.4): READ row 3 -- be3=0.05, everything else 0.
* t=[2.4,2.9): READ row 4 -- be4=0.05, everything else 0.
* Every transition uses a real 1us ramp (ngspice's own PWL parser
* rejects two points at the same time as "non-increasing", the same
* real, found-live issue the 2x2 deck's own testbench already
* documents). Only ONE real write phase -- writing more than one real
* diagonal cell was already found, for 2x2, to give off-diagonal cells
* a real cumulative disturb exposure that erases the real gap this
* deck exists to show; the same real reasoning applies here unchanged.
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
wrdata crossbar4x4_write_read_extracted.csv v(be1) v(be2) v(be3) v(be4) v(te1) v(te2) v(te3) v(te4) i(vte1) i(vte2) i(vte3) i(vte4)
.endc
.end
