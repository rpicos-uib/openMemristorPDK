v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Memristor testbench} -60 -300 0 0 0.6 0.6 {}
T {Press "Netlist", then "Simulate" (top-right of the menu bar).} -60 -240 0 0 0.3 0.3 {}
T {The sine-wave source V1 pushes current back and forth through the memristor n1.} -60 -210 0 0 0.3 0.3 {}
N 40 -100 400 -100 {lab=te}
N 400 -40 400 -20 {lab=0}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_tio2_au.sym} 0 -100 0 1 {name=n1 model=mm}
C {gnd.sym} -40 -100 0 0 {name=l1 lab=0}
C {lab_wire.sym} 220 -100 0 0 {name=p1 sig_type=std_logic lab=te}
C {vsource.sym} 400 -70 0 0 {name=V1 value="dc 0 sin(0 1.0 0.6)" savecurrent=false}
C {gnd.sym} 400 -20 0 0 {name=l2 lab=0}
C {code_shown.sym} -60 40 0 0 {name=s1 only_toplevel=false value="
.model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0
.control
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_tio2_au.osdi
tran 300u 3.34
plot -i(V1) vs v(te) retraceplot title 'Memristor I-V loop' xlabel 'Voltage (V)' ylabel 'Current (A)'
.endc
"}
