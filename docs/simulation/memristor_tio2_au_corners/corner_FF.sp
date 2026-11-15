Au/TiO2/Au memristor -- FF corner transient
.lib ../../../data/openmemristorpdk/libs.tech/ngspice/models/openmemristorpdk_corners.lib FF
.model mm memristor_tio2_au ron={ron_tio2_au} roff={roff_tio2_au} d=10n uv=1e-14 x0=0
n1 te 0 mm
vte te 0 dc 0 sin(0 1.0 0.6)
.tran 300u 3.34
.control
run
wrdata corner_FF.csv v(te) i(vte)
.endc
.end
