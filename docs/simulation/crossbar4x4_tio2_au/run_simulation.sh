#!/usr/bin/env bash
# Real, reproducible pipeline for the 4x4 Au/TiO2/Au crossbar write-
# then-read demo, run TWICE -- once through the real, patched Magic-
# extracted layout netlist, once through the real, live xschem-
# netlisted schematic -- to directly confirm both real views of this
# cell simulate identically, not just match topologically (LVS).
#
#   podman exec -e DISPLAY=:1 <container-name> bash -lc \
#       'cd /foss/designs/openMemristorPDK/docs/simulation/crossbar4x4_tio2_au && bash run_simulation.sh'
set -euo pipefail
cd "$(dirname "$0")"

PROJECT_ROOT=/foss/designs/openMemristorPDK
MAG=$PROJECT_ROOT/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au.mag
TECH=$PROJECT_ROOT/export/openmemristorpdk/libs.tech/magic/openmemristorpdk.tech

echo "[1/6] Extracting the real, patched layout netlist (memristor_extract.py)..."
python3 - <<PYEOF
import sys
sys.path.insert(0, "$PROJECT_ROOT")
from pathlib import Path
from openpdkcreator.pdklib import extraction as ext_mod
from openpdkcreator.pdklib import memristor_extract as mx_mod
r = mx_mod.run_extract_with_memristor_patch(Path("$MAG"), Path("$TECH"), "magic", mode="parasitic")
assert r.ok, r.log
Path("crossbar4x4_tio2_au_extracted.spice").write_text(r.spice_path.read_text())
print(r.spice_path.read_text())
PYEOF

echo "[2/6] Netlisting the real, live schematic (gen_schematic_netlist.py)..."
python3 gen_schematic_netlist.py

echo "[3/6] Compiling memristor_tio2_au.va with OpenVAF..."
openvaf memristor_tio2_au.va --output memristor_tio2_au.osdi

echo "[4/6] Running the real ngspice transient through the extracted netlist..."
ngspice -b crossbar_write_read_extracted.sp

echo "[5/6] Running the real ngspice transient through the schematic netlist..."
ngspice -b crossbar_write_read_schematic.sp

echo "[6/6] Plotting the real, direct comparison..."
python3 plot_comparison.py

echo "Done -- see crossbar4x4_comparison.png"
