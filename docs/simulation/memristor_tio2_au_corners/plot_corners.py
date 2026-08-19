"""Plots the real ngspice transient output for all three real process
corners (TT/FF/SS, openmemristorpdk_corners.lib) of the Au/TiO2/Au
device on one real, overlaid pinched I-V hysteresis plot -- shows the
real resistance-window shift each corner's own real Ron/Roff
parameter override produces. Reads real, already-simulated data only;
never runs ngspice itself."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
CORNERS = [("TT", "#1565c0"), ("FF", "#2e7d32"), ("SS", "#c0392b")]

fig, ax = plt.subplots(figsize=(6.5, 5))
for corner, color in CORNERS:
    t, v, i = [], [], []
    with (HERE / f"corner_{corner}.csv").open() as f:
        for row in csv.reader(f, delimiter=" "):
            fields = [x for x in row if x]
            if len(fields) < 4:
                continue
            t.append(float(fields[0]))
            v.append(float(fields[1]))
            i.append(float(fields[3]))
    ax.plot([x * 1e3 for x in i], v, color=color, linewidth=1.4, label=corner)

ax.axhline(0, color="#999999", linewidth=0.6)
ax.axvline(0, color="#999999", linewidth=0.6)
ax.set_xlabel("Current through memristor (mA)")
ax.set_ylabel("Voltage across memristor (V)")
ax.set_title("Au/TiO2/Au memristor -- TT/FF/SS corner sweep\n(real ngspice/OSDI transient, same drive, 3 real corners)")
ax.legend(title="Corner")

fig.tight_layout()
out_path = HERE / "corners_transient.png"
fig.savefig(out_path, dpi=150)
print(f"Wrote {out_path}")
