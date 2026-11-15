Au/TiO2/Ti memristor -- transient, pinched hysteresis
.model mm memristor_tio2_ti ron=250 roff=20k d=10n uv=0.8e-14 x0=0
n1 te 0 mm
vte te 0 dc 0 sin(0 1.0 0.6)
.tran 300u 3.34
.control
run
wrdata memristor_tran.csv v(te) i(vte)
.endc
.end
