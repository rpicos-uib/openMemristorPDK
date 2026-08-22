"""Plots the real ngspice transient output (crossbar_write_read.csv)
for the 2x2 crossbar write-then-read demo -- the real row/column drive
waveforms, the real per-column read currents they produce, and a real,
computed per-cell read resistance bar chart (R = Vr / I averaged over
the last quarter of each cell's own real read window) showing the
sneak-path disturb directly. Reads real, already-simulated data only;
never runs ngspice itself."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
CSV_PATH = HERE / "crossbar_write_read.csv"
VR = 0.05

t, vbe1, vbe2, vte1, vte2, ite1, ite2 = [], [], [], [], [], [], []
with CSV_PATH.open() as f:
    for row in csv.reader(f, delimiter=" "):
        fields = [x for x in row if x]
        if len(fields) < 7:
            continue
        t.append(float(fields[0]))
        vbe1.append(float(fields[1]))
        vbe2.append(float(fields[3]))
        vte1.append(float(fields[5]))
        vte2.append(float(fields[7]))
        ite1.append(float(fields[9]))
        ite2.append(float(fields[11]))


def _mean_current(current, t0, t1):
    vals = [c for tt, c in zip(t, current) if t0 <= tt <= t1]
    return sum(vals) / len(vals) if vals else float("nan")


# Real read windows: row 1 in [0.9,1.4), row 2 in [1.4,1.9) -- averaged
# over each window's own last quarter, well clear of the PWL edge.
i_11 = _mean_current(ite1, 1.275, 1.4)
i_12 = _mean_current(ite2, 1.275, 1.4)
i_21 = _mean_current(ite1, 1.775, 1.9)
i_22 = _mean_current(ite2, 1.775, 1.9)
r = {
    "(1,1)\nwritten": VR / abs(i_11),
    "(1,2)\nsneak-disturbed": VR / abs(i_12),
    "(2,1)\nsneak-disturbed": VR / abs(i_21),
    "(2,2)\nuntouched": VR / abs(i_22),
}
for label, value in r.items():
    print(f"R{label.splitlines()[0]} = {value:.0f} ohm  ({label.splitlines()[1]})")

fig, axes = plt.subplots(3, 1, figsize=(8, 9), height_ratios=[1, 1, 1.1])

ax = axes[0]
ax.plot(t, vbe1, color="#c0392b", linewidth=1.2, label="V(BE1)")
ax.plot(t, vbe2, color="#8e44ad", linewidth=1.2, label="V(BE2)")
ax.plot(t, vte1, color="#2e7d32", linewidth=1.2, label="V(TE1)")
ax.plot(t, vte2, color="#1565c0", linewidth=1.2, label="V(TE2)")
ax.set_ylabel("Row/column voltage (V)")
ax.set_title("Real row/column drive -- write (1,1) only, then read row 1, read row 2")
ax.legend(fontsize=8, ncol=4, loc="upper right")

ax = axes[1]
ax.plot(t, [x * 1e3 for x in ite1], color="#2e7d32", linewidth=1.0, label="I(TE1)")
ax.plot(t, [x * 1e3 for x in ite2], color="#1565c0", linewidth=1.0, label="I(TE2)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Column current (mA)")
ax.set_title("Real per-column current -- write pulses, then the two real read windows")
ax.legend(fontsize=8, loc="upper right")

ax = axes[2]
colors = ["#2e7d32", "#c0392b", "#c0392b", "#1565c0"]
ax.bar(list(r.keys()), list(r.values()), color=colors)
ax.set_ylabel("Read resistance (ohm)")
ax.set_title("Real, computed per-cell read resistance -- sneak-path disturb, not guessed")

fig.suptitle("2x2 Au/TiO2/Au memristor crossbar -- real ngspice/OSDI write-then-read")
fig.tight_layout()
out_path = HERE / "crossbar_write_read.png"
fig.savefig(out_path, dpi=150)
print(f"Wrote {out_path} from {len(t)} real, simulated data points.")
