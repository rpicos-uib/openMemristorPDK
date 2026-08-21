v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_hfo2_al.sym} 0 0 0 0 {name=n1 model=mm}
C {gnd.sym} -40 0 0 0 {name=l1 lab=0}
C {vsource.sym} 200 -30 0 0 {name=V1 value="dc 0 sin(0 1.2 25)"}
C {gnd.sym} 200 -60 0 0 {name=l2 lab=0}
C {code_shown.sym} 0 -150 0 0 {name=s1 only_toplevel=false value=".model mm memristor_hfo2_al ron=500 roff=50k von=0.8 voff=-0.6 tau=1m x0=0.1"}
N 40 0 200 0 {}
