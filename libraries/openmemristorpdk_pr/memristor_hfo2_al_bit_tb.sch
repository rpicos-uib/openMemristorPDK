v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {One memristor, one bit} -60 -300 0 0 0.6 0.6 {}
T {Press "Netlist", then "Simulate" (top-right of the menu bar).} -60 -240 0 0 0.3 0.3 {}
T {V1 reads, writes a 1, reads, writes a 0 and reads again: 100 ns for each.} -60 -210 0 0 0.3 0.3 {}
N 40 -100 400 -100 {lab=te}
N 400 -40 400 -20 {lab=0}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 0 -100 0 1 {name=n1 model=mm}
C {gnd.sym} -40 -100 0 0 {name=l1 lab=0}
C {lab_wire.sym} 220 -100 0 0 {name=p1 sig_type=std_logic lab=te}
C {vsource.sym} 400 -70 0 0 {name=V1 value="pwl(0 0 10n 0.2 90n 0.2 100n 0 110n \{vset\} 190n \{vset\} 200n 0 210n 0.2 290n 0.2 300n 0 310n \{vreset\} 390n \{vreset\} 400n 0 410n 0.2 490n 0.2 500n 0)" savecurrent=false}
C {gnd.sym} 400 -20 0 0 {name=l2 lab=0}
C {code_shown.sym} -60 40 0 0 {name=s1 only_toplevel=false value="
* vset writes a 1, vreset writes a 0. Reading uses 0.2 V.
.param vset = 1.2
.param vreset = -1.0
.model mm memristor_hfo2_al ron=500 roff=50k von=0.8 voff=-0.6 tau=5n x0=0
.control
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_hfo2_al.osdi
tran 0.5n 500n
let imem = -i(V1) * 1e6
meas tran read1 avg imem from=40n to=80n
meas tran read2 avg imem from=240n to=280n
meas tran read3 avg imem from=440n to=480n
echo
echo read 1  before any write:  $&read1 uA
echo read 2  after write 1:     $&read2 uA
echo read 3  after write 0:     $&read3 uA
plot v(te) title 'Voltage on the memristor' xlabel 'Time (s)' ylabel 'Voltage (V)'
plot -i(V1) title 'Current through the memristor' xlabel 'Time (s)' ylabel 'Current (A)'
.endc
"}
