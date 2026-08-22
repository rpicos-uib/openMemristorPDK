#!/usr/bin/env bash
# Real, reproducible pipeline for the 2x2 Au/TiO2/Au crossbar write-
# then-read demo -- run from inside the IIC-OSIC-TOOLS container
# (openvaf/ngspice/python3 with matplotlib all live there).
#
#   podman exec -e DISPLAY=:1 <container-name> bash -lc \
#       'cd /foss/designs/openMemristorPDK/docs/simulation/crossbar2x2_tio2_au && bash run_simulation.sh'
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/3] Compiling memristor_tio2_au.va with OpenVAF..."
openvaf memristor_tio2_au.va --output memristor_tio2_au.osdi

echo "[2/3] Running the real ngspice transient (crossbar_write_read.sp)..."
ngspice -b crossbar_write_read.sp

echo "[3/3] Plotting the real, simulated output..."
python3 plot_crossbar.py

echo "Done -- see crossbar_write_read.png"
