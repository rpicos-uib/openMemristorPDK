tech load /foss/designs/openMemristorPDK/data/openmemristorpdk/libs.tech/magic/openmemristorpdk.tech
cd /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr
load crossbar2x2_tio2_au
select top cell
port renumber
extract no all
extract all
ext2spice lvs
ext2spice -o /foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar2x2_tio2_au_lvs.spice
quit -noprompt
