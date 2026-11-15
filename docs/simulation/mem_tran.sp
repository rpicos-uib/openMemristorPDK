HP linear ion-drift memristor -- transient, pinched hysteresis
.model mm hp_memristor ron=100 roff=16k d=10n uv=1e-14 x0=0
n1 te 0 mm
vte te 0 dc 0 sin(0 1.0 0.6)
.tran 300u 3.34
.control
run
wrdata memristor_tran.csv v(te) i(vte)
.endc
.end
