v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {A real bit-cell: one transistor, one memristor (1T1R)} -260 -520 0 0 0.6 0.6 {}
T {Press "Netlist", then "Simulate" (top-right of the menu bar).} -260 -460 0 0 0.3 0.3 {}
T {The transistor comes from the IHP SG13G2 PDK; the memristor from openMemristorPDK.} -260 -430 0 0 0.3 0.3 {}
N -160 -320 200 -320 {lab=bl}
N 200 -320 200 -280 {lab=bl}
C {vsource.sym} -160 -290 0 0 {name=VBL value="pwl(0 0 10n 0.2 90n 0.2 100n 0 110n \{vset\} 190n \{vset\} 200n 0 210n 0.2 290n 0.2 300n 0 310n \{vset\} 390n \{vset\} 400n 0 410n 0.2 490n 0.2 500n 0 600n 0 610n 0.2 690n 0.2 700n 0)" savecurrent=false}
C {gnd.sym} -160 -260 0 0 {name=l1 lab=0}
C {lab_wire.sym} 20 -320 0 0 {name=p1 sig_type=std_logic lab=bl}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 200 -240 1 0 {name=n1 model=mm}
N 200 -200 200 -170 {lab=m}
C {lab_wire.sym} 200 -185 0 0 {name=p2 sig_type=std_logic lab=m}
C {/foss/pdks/ihp-sg13g2/libs.tech/xschem/sg13g2_pr/sg13_hv_nmos.sym} 180 -140 0 0 {name=M1 l=0.45u w=5u ng=1 m=1 model=sg13_hv_nmos spiceprefix=X}
N 200 -140 260 -140 {lab=0}
C {gnd.sym} 260 -140 0 0 {name=l2 lab=0}
N -40 -140 160 -140 {lab=wl}
C {vsource.sym} -40 -110 0 0 {name=VWL value="pwl(0 \{vwl\} 95n \{vwl\} 100n 0 200n 0 205n \{vwl\} 700n \{vwl\})" savecurrent=false}
C {gnd.sym} -40 -80 0 0 {name=l3 lab=0}
C {lab_wire.sym} 60 -140 0 0 {name=p3 sig_type=std_logic lab=wl}
N 200 -110 200 -60 {lab=sl}
C {lab_wire.sym} 200 -85 0 0 {name=p4 sig_type=std_logic lab=sl}
C {vsource.sym} 200 -30 0 0 {name=VSL value="pwl(0 0 500n 0 510n \{vreset\} 590n \{vreset\} 600n 0 700n 0)" savecurrent=false}
C {gnd.sym} 200 0 0 0 {name=l4 lab=0}
C {code_shown.sym} -260 60 0 0 {name=s1 only_toplevel=false value="
* wl opens the transistor (the door); bl writes 1 and reads; sl writes 0.
.param vwl = 3.3
.param vset = 1.5
.param vreset = 2.0
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
.model mm memristor_hfo2_al ron=500 roff=50k von=0.8 voff=-0.6 tau=5n x0=0
.control
pre_osdi /foss/pdks/ihp-sg13g2/libs.tech/ngspice/osdi/psp103.osdi
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_hfo2_al.osdi
tran 0.5n 700n
let imem = -i(VBL) * 1e6
meas tran read1 avg imem from=40n to=80n
meas tran read2 avg imem from=240n to=280n
meas tran read3 avg imem from=440n to=480n
meas tran read4 avg imem from=640n to=680n
echo
echo read 1  before any write:           $&read1 uA
echo read 2  after write 1 (door shut):  $&read2 uA
echo read 3  after write 1 (door open):  $&read3 uA
echo read 4  after write 0:              $&read4 uA
plot v(wl) v(bl) v(sl) title 'Word line - bit line - source line' ylabel 'Voltage (V)'
plot -i(VBL) title 'Current into the bit line' ylabel 'Current (A)'
.endc
"}
