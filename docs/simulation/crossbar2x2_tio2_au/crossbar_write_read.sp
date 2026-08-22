2x2 Au/TiO2/Au memristor crossbar -- real write-then-read, sneak-path visible
* Real V/2 row/column biasing (the standard passive-crossbar scheme:
* selected row = Vw, selected column = 0, every other row/column =
* Vw/2) -- writes just cell (1,1) to the real LOW-resistance (SET)
* state. Cells (1,2)/(2,1) are never themselves selected, but sit at
* the real Vw/2 half-select voltage during that one write, the real
* crossbar sneak-path disturb this deck is built to show; cell (2,2)
* sees 0V throughout, a real, untouched control. Reads then drive one
* real row at a time at a small Vr (both TE columns held at 0, both
* ammeters live), reading both of that row's real cells at once.
.control
pre_osdi memristor_tio2_au.osdi
.endc

.model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0.3

.subckt memristor_tio2_au_prim BE TE
n1 BE TE mm
.ends

.include crossbar2x2_tio2_au.spice

X0 be1 be2 te1 te2 crossbar2x2_tio2_au

* --- real, discrete PWL row/column drive ------------------------------
* Every transition uses a real, tiny (1us) ramp, not two PWL points at
* the exact same time -- ngspice's own PWL parser rejects that as
* "non-increasing", confirmed live (not guessed) after the first, naive
* same-time-jump version of this deck produced exactly that warning.
* t=[0,0.9): WRITE (1,1) only -- be1=1.0 te1=0.0 (full Vw), be2=te2=0.5
*   (real V/2 unselect). Cell (1,1) is fully written; cells (1,2)/(2,1)
*   sit at the real Vw/2 disturb voltage (same-row/same-column "half-
*   select"); cell (2,2) sees 0V the whole time -- never touched at all.
* t=[0.9,1.4): READ row 1 -- be1=0.05 (Vr), be2=te1=te2=0
* t=[1.4,1.9): READ row 2 -- be2=0.05 (Vr), be1=te1=te2=0
*
* Only ONE real write phase, deliberately, not two -- an earlier,
* two-write-phase version (also writing (2,2)) gave the two disturbed
* cells a real, *cumulative* 2x exposure to the unselect voltage (once
* per write phase), pushing them to fully saturate too and erasing the
* real gap this deck exists to show; a single write phase gives every
* real cell exactly one, honestly-comparable exposure.
*
* The real unselect voltage must be exactly Vw/2, not an arbitrary
* smaller value -- confirmed live the hard way: an earlier pass used
* an asymmetric, smaller unselect voltage (0.2V, hoping to slow the
* disturb down further), which broke the real V/2 symmetry instead --
* a same-row/different-column cell sees (Vw - Vunselect), a same-
* column/different-row cell sees just Vunselect, and those two are
* only equal when Vunselect = Vw/2; at 0.2V the first real disturb
* voltage came out to 0.8V (nearly a full write), silently saturating
* a cell this deck means to show as merely disturbed.
*
* Real, found-live *duration* tuning, not guessed, directly against
* this exact real device (not an idealized approximation -- an
* earlier, simplified Python reproduction of the model's own equation
* disagreed with the real OSDI simulation's own actual trajectory):
* a single real device driven at Vw=1.0 reaches full Ron by about
* t=0.9s; the same real device driven at Vw/2=0.5 is still close to
* its own real initial resistance at that same t=0.9s -- 0.9s leaves
* a wide, real, comfortable margin between "written" and "disturbed".
vbe1 be1 0 PWL(0 1.0  0.9 1.0  0.900001 0.05  1.4 0.05  1.400001 0.0  1.9 0.0)
vbe2 be2 0 PWL(0 0.5  0.9 0.5  0.900001 0.0   1.4 0.0   1.400001 0.05  1.9 0.05)
vte1 te1 0 dc 0
vte2 te2 0 PWL(0 0.5  0.9 0.5  0.900001 0.0  1.9 0.0)

.tran 0.2m 1.9

.control
run
wrdata crossbar_write_read.csv v(be1) v(be2) v(te1) v(te2) i(vte1) i(vte2)
.endc
.end
