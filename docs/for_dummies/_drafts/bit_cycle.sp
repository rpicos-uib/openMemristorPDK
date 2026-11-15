one memristor as one bit
.model mm memristor_hfo2_al x0=0
n1 te 0 mm
* read 0.2 V, write 1 (SET +1.2 V), read, write 0 (RESET -1.0 V), read
vte te 0 pwl(0 0  10n 0.2  90n 0.2  100n 0  110n 1.2  190n 1.2  200n 0
+ 210n 0.2  290n 0.2  300n 0  310n -1.0  390n -1.0  400n 0  410n 0.2  490n 0.2  500n 0)
.control
pre_osdi /foss/designs/openMemristorPDK/user_models/veriloga/memristor_hfo2_al.osdi
tran 0.5n 500n
let imem = -vte#branch*1e6
meas tran r0 avg imem from=40n to=80n
meas tran r1 avg imem from=240n to=280n
meas tran r2 avg imem from=440n to=480n
wrdata bit.csv v(te) imem
.endc
.end
