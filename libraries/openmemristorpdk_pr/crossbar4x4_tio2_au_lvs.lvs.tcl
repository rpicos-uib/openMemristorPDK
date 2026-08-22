set circuit1 [readnet spice /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au_lvs.spice]
set circuit2 [readnet spice /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au.cdl]
lvs "$circuit1 crossbar4x4_tio2_au" "$circuit2 crossbar4x4_tio2_au" /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au_lvs.lvs_setup.tcl /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au_lvs.lvs_report.out
quit
