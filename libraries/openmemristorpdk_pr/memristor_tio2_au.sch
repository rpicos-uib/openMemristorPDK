v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 40 0 200 0 {lab=#net1}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_tio2_au.sym} 0 0 0 0 {name=n1 model=mm
view=extracted}
C {gnd.sym} -40 0 0 0 {name=l1 lab=0}
C {vsource.sym} 200 -30 0 0 {name=V1 value="dc 0 sin(0 1.0 0.6)"}
C {gnd.sym} 200 -60 0 0 {name=l2 lab=0}
C {code_shown.sym} 0 -150 0 0 {name=s1 only_toplevel=false value=".model mm memristor_tio2_au ron=100 roff=16k d=10n uv=1e-14 x0=0.3"}
