Au/HfO2/Al memristor -- bipolar threshold-switching transient
.model mm memristor_hfo2_al ron=500 roff=50k von=0.8 voff=-0.6 tau=1m x0=0.1
n1 te 0 mm
vte te 0 dc 0 sin(0 1.2 25)
.tran 20u 80m
.control
run
wrdata memristor_tran.csv v(te) i(vte)
.endc
.end
