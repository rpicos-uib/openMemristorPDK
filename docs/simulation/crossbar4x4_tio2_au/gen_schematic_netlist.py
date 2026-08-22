"""Generates crossbar4x4_tio2_au_schematic.spice -- a real, simulatable
`.subckt crossbar4x4_tio2_au BE1 BE2 BE3 BE4 TE1 TE2 TE3 TE4 ... .ends`
wrapper around the real device lines real, live xschem itself produces
when batch-netlisting crossbar4x4_tio2_au.sch (the same real
schematic already verified in tests/test_crossbar4x4.py to carry all
16 real devices, correct real row/column pairing).

Not a hand-transcription: the real `n... BE_i TE_j mm` lines are
parsed directly out of real xschem's own real batch output
(`xschem -n -s -q`) -- only the outer `.subckt`/port-order/`.ends`
wrapper (xschem's own default netlist for this schematic never emits
one for the *top* cell, only for subcells -- confirmed live, its own
`**.subckt .../ **.ends` lines are left commented out unless a real
`subcircuit top on` preference is set) is added here, so this file's
own top-level port order (BE1..BE4, TE1..TE4) matches the real,
extracted-view netlist's own port order exactly, letting the same
real testbench call either one interchangeably."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/foss/designs/openMemristorPDK")
from openpdkcreator.pdklib import tool_env
from openpdkcreator.pdklib import xschem_view_switch as xvs_mod

PDK_ROOT = Path("/foss/designs/openMemristorPDK/data/openmemristorpdk")
SCH_PATH = Path("/foss/designs/openMemristorPDK/libraries/openmemristorpdk_pr/crossbar4x4_tio2_au.sch")
OUT_PATH = Path(__file__).parent / "crossbar4x4_tio2_au_schematic.spice"

PORTS = ["BE1", "BE2", "BE3", "BE4", "TE1", "TE2", "TE3", "TE4"]

rcfile = tool_env.xschem_rcfile(PDK_ROOT)
netlist_text, log = xvs_mod.run_netlist(SCH_PATH, "xschem", rcfile)
if netlist_text is None:
    raise RuntimeError(f"real xschem batch netlist failed:\n{log}")

device_lines = []
for line in netlist_text.splitlines():
    parts = line.split()
    if len(parts) == 4 and parts[0].startswith("n") and parts[0][1:].isdigit():
        device_lines.append(f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}")

if len(device_lines) != 16:
    raise RuntimeError(f"expected 16 real device lines from xschem, found {len(device_lines)}:\n{netlist_text}")

out_lines = [
    f".subckt crossbar4x4_tio2_au {' '.join(PORTS)}",
    *device_lines,
    ".ends",
]
OUT_PATH.write_text("\n".join(out_lines) + "\n")
print(f"Wrote {OUT_PATH} from {len(device_lines)} real, live xschem-netlisted devices.")
