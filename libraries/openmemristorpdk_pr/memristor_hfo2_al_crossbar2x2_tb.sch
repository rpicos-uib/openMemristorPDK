v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {A 2 x 2 crossbar: four bits} -60 -800 0 0 0.6 0.6 {}
T {Press "Netlist", then "Simulate" (top-right of the menu bar).} -60 -740 0 0 0.3 0.3 {}
T {Writes 1 into the top-left and bottom-right memristors, then reads all four.} -60 -710 0 0 0.3 0.3 {}
N 0 -560 0 -40 {lab=be1}
C {lab_wire.sym} 0 -560 0 0 {name=lc1 sig_type=std_logic lab=be1}
N 300 -560 300 -120 {lab=be2}
C {lab_wire.sym} 300 -560 0 0 {name=lc2 sig_type=std_logic lab=be2}
N -60 -400 500 -400 {lab=te1}
C {lab_wire.sym} -40 -400 0 0 {name=lr1 sig_type=std_logic lab=te1}
N -60 -200 500 -200 {lab=te2}
C {lab_wire.sym} -40 -200 0 0 {name=lr2 sig_type=std_logic lab=te2}
N 0 -480 80 -480 {lab=be1}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 80 -440 1 0 {name=n11 model=mm}
T {cell 11} 100 -450 0 0 0.25 0.25 {}
N 300 -480 380 -480 {lab=be2}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 380 -440 1 0 {name=n12 model=mm}
T {cell 12} 400 -450 0 0 0.25 0.25 {}
N 0 -280 80 -280 {lab=be1}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 80 -240 1 0 {name=n21 model=mm}
T {cell 21} 100 -250 0 0 0.25 0.25 {}
N 300 -280 380 -280 {lab=be2}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 380 -240 1 0 {name=n22 model=mm}
T {cell 22} 400 -250 0 0 0.25 0.25 {}
C {vsource.sym} 0 -10 0 0 {name=VBE1 value="pwl(0 0 10n \{vcol\} 90n \{vcol\} 100n 0 200n 0 210n 0.2 290n 0.2 300n 0 400n 0 410n 0.2 490n 0.2 500n 0 600n 0)" savecurrent=false}
C {gnd.sym} 0 20 0 0 {name=gb1 lab=0}
C {vsource.sym} 300 -90 0 0 {name=VBE2 value="pwl(0 0 100n 0 110n \{vcol\} 190n \{vcol\} 200n 0 300n 0 310n 0.2 390n 0.2 400n 0 500n 0 510n 0.2 590n 0.2 600n 0)" savecurrent=false}
C {gnd.sym} 300 -60 0 0 {name=gb2 lab=0}
C {vsource.sym} 500 -370 0 0 {name=VTE1 value="pwl(0 0 10n \{vrow\} 90n \{vrow\} 100n 0 600n 0)" savecurrent=false}
C {gnd.sym} 500 -340 0 0 {name=gt1 lab=0}
C {vsource.sym} 500 -170 0 0 {name=VTE2 value="pwl(0 0 100n 0 110n \{vrow\} 190n \{vrow\} 200n 0 600n 0)" savecurrent=false}
C {gnd.sym} 500 -140 0 0 {name=gt2 lab=0}
C {code_shown.sym} 700 -900 0 0 {name=s1 only_toplevel=false value="
* A write puts 1.2 V across one memristor: column minus row.
* colpart = 0.5: +0.6 V on the column, -0.6 V on the row.
.param colpart = 0.5
.param vcol = \{1.2 * colpart\}
.param vrow = \{-1.2 * (1 - colpart)\}
.model mm memristor_hfo2_al ron=500 roff=50k von=0.8 voff=-0.6 tau=5n x0=0
.control
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_hfo2_al.osdi
tran 0.5n 600n
let i1 = i(VTE1) * 1e6
let i2 = i(VTE2) * 1e6
meas tran c11 avg i1 from=240n to=280n
meas tran c12 avg i1 from=340n to=380n
meas tran c21 avg i2 from=440n to=480n
meas tran c22 avg i2 from=540n to=580n
echo
echo reads in uA (more than 100 means 1):
echo row 1:   cell 11 = $&c11    cell 12 = $&c12
echo row 2:   cell 21 = $&c21    cell 22 = $&c22
* The row being read: row 1, then row 2.
let readcur = i(VTE1) * (time < 400e-9) + i(VTE2) * (time >= 400e-9)
settype current readcur
plot readcur xlimit 200e-9 600e-9 title 'Read current' ylabel 'Current (A)'
.endc
"}
