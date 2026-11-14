v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Memristor Monte Carlo} -60 -300 0 0 0.6 0.6 {}
T {Press "Netlist", then "Simulate" (top-right of the menu bar).} -60 -240 0 0 0.3 0.3 {}
T {The code block below simulates 20 memristors with random Ron, Roff and oxide thickness D.} -60 -210 0 0 0.3 0.3 {}
N 40 -100 400 -100 {lab=te}
N 400 -40 400 -20 {lab=0}
C {/foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/xschem/openmemristorpdk_pr/memristor_tio2_au.sym} 0 -100 0 1 {name=n1 model=mm}
C {gnd.sym} -40 -100 0 0 {name=l1 lab=0}
C {lab_wire.sym} 220 -100 0 0 {name=p1 sig_type=std_logic lab=te}
C {vsource.sym} 400 -70 0 0 {name=V1 value="dc 0 sin(0 1.0 0.6)" savecurrent=false}
C {gnd.sym} 400 -20 0 0 {name=l2 lab=0}
C {code_shown.sym} -60 40 0 0 {name=s1 only_toplevel=false value="
* Monte Carlo: simulate 20 memristors, each one a little different,
* like 20 devices from a real factory. agauss(typical, spread, 1)
* draws a random value around the typical one (a bell curve).
.param ron_mc  = agauss(100, 10, 1)
.param roff_mc = agauss(16k, 1.6k, 1)
.param d_mc    = agauss(10n, 0.5n, 1)
.model mm memristor_tio2_au ron=\{ron_mc\} roff=\{roff_mc\} d=\{d_mc\} uv=1e-14 x0=0.3
.options interp
.control
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_tio2_au.osdi
* setseed: the same 20 random memristors every time (the ones in the guide)
setseed 16
let runs = 20
let ron = vector(runs)
let roff = vector(runs)
let dnm = vector(runs)
let peak = vector(runs)
set curves = ( )
let n = 0
dowhile n < runs
  reset
  tran 1m 3.34
  let ron[n] = @mm[ron]
  let roff[n] = @mm[roff]
  let dnm[n] = @mm[d] * 1e9
  let imem = -i(V1)
  let peak[n] = maximum(imem) * 1e6
  set curves = ( $curves \{$curplot\}.imem )
  let n = n + 1
end
setplot const
let n = 0
dowhile n < runs
  let r1 = ron[n]
  let r2 = roff[n]
  let dd = dnm[n]
  let pk = peak[n]
  echo memristor $&n :  Ron $&r1  Roff $&r2  D $&dd nm  peak $&pk uA
  let n = n + 1
end
plot $curves vs tran1.v(te) retraceplot title '20 memristors (Monte Carlo)' xlabel 'Voltage (V)' ylabel 'Current (A)'
.endc
"}
