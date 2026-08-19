#!/usr/bin/env bash
# Real, reproducible pipeline for the Au/TiO2/Au memristor demo -- run
# from inside the IIC-OSIC-TOOLS container (openvaf/ngspice/python3
# with matplotlib all live there).
#
#   podman exec -e DISPLAY=:1 <container-name> bash -lc \
#       'cd /foss/designs/openMemristorPDK/docs/simulation/memristor_tio2_au && bash run_simulation.sh'
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/3] Compiling memristor_tio2_au.va with OpenVAF..."
openvaf memristor_tio2_au.va --output memristor_tio2_au.osdi

echo "[2/3] Running the real ngspice transient (mem_tran.sp)..."
ngspice -b mem_tran.sp

echo "[3/3] Plotting the real, simulated output..."
python3 plot_memristor.py

echo "Done -- see memristor_transient.png"
