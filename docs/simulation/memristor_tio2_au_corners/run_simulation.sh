#!/usr/bin/env bash
# Real, reproducible pipeline for the Au/TiO2/Au TT/FF/SS corner sweep
# demo -- run from inside the IIC-OSIC-TOOLS container (openvaf/
# ngspice/python3 with matplotlib all live there).
#
#   podman exec -e DISPLAY=:1 <container-name> bash -lc \
#       'cd /foss/designs/openMemristorPDK/docs/simulation/memristor_tio2_au_corners && bash run_simulation.sh'
set -euo pipefail
cd "$(dirname "$0")"

echo "[1/3] Compiling memristor_tio2_au.va with OpenVAF..."
openvaf memristor_tio2_au.va --output memristor_tio2_au.osdi

echo "[2/3] Running the real ngspice transient for each real corner (TT/FF/SS)..."
for corner in TT FF SS; do
    ngspice -b "corner_${corner}.sp"
done

echo "[3/3] Plotting the real, simulated output..."
python3 plot_corners.py

echo "Done -- see corners_transient.png"
