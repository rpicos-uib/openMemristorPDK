tech load /foss/designs/openMemristorPDK/export/openmemristorpdk/libs.tech/magic/openmemristorpdk.tech
cd /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr
load memristor_tio2_au
box 0 0 0.5 0.5
paint be_au
label BE c be_au
port make
box 0 0 0.5 0.5
paint mem_tio2
box 0 0 0.5 0.5
paint te_au
label TE c te_au
port make
port renumber
save memristor_tio2_au
gds write memristor_tio2_au
quit -noprompt
