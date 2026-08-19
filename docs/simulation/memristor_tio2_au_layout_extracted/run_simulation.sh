#!/usr/bin/env bash
# Real, reproducible pipeline: layout -> real Magic extraction -> real
# ngspice simulation of the extracted netlist, for memristor_tio2_au.
# Run from inside the IIC-OSIC-TOOLS container:
#
#   podman exec -e DISPLAY=:1 <container-name> bash -lc \
#       'cd /foss/designs/openMemristorPDK/docs/simulation/memristor_tio2_au_layout_extracted && bash run_simulation.sh'
set -euo pipefail
cd "$(dirname "$0")"

PROJECT_ROOT=/foss/designs/openMemristorPDK
MAG=$PROJECT_ROOT/libraries/openmemristorpdk_pr/memristor_tio2_au.mag
TECH=$PROJECT_ROOT/export/openmemristorpdk/libs.tech/magic/openmemristorpdk.tech

echo "[1/4] Extracting the real Magic layout via openpdkcreator's own real Extract to SPICE..."
python3 - <<PYEOF
import sys
sys.path.insert(0, "$PROJECT_ROOT")
from pathlib import Path
from openpdkcreator.pdklib import extraction as ex
r = ex.run_extract(Path("$MAG"), Path("$TECH"), "magic", mode="parasitic")
assert r.ok, r.log
Path("memristor_tio2_au_extracted.spice").write_text(r.spice_path.read_text())
print(r.spice_path.read_text())
PYEOF

echo "[2/4] Compiling memristor_tio2_au.va with OpenVAF..."
openvaf "$PROJECT_ROOT/user_models/veriloga/memristor_tio2_au.va" --output memristor_tio2_au.osdi

echo "[3/4] Running the real ngspice transient through the real extracted netlist..."
ngspice -b mem_tran_extracted.sp

echo "[4/4] Done -- see memristor_extracted_tran.csv"
