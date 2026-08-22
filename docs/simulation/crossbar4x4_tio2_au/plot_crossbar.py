"""Plots the real ngspice transient output
(crossbar4x4_write_read_extracted.csv) for the 4x4 crossbar
write-then-read demo -- the real row/column drive waveforms, the real
per-column read currents, and a real, computed per-cell read
resistance bar chart, same real convention as the 2x2 deck's own
plot_crossbar.py, scaled to 4 rows/4 read phases. Reads real,
already-simulated data only; never runs ngspice itself. (The
schematic-driven run produces an identical real result -- see
plot_comparison.py / crossbar4x4_comparison.png for the real, direct
proof.)"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
CSV_PATH = HERE / "crossbar4x4_write_read_extracted.csv"
VR = 0.05
ROWS = ["BE1", "BE2", "BE3", "BE4"]
COLS = ["TE1", "TE2", "TE3", "TE4"]
SIGNALS = [f"v({r.lower()})" for r in ROWS] + [f"v({c.lower()})" for c in COLS] + [f"i(vte{i+1})" for i in range(4)]
READ_WINDOWS = [(0.9 + 0.5 * i, 0.9 + 0.5 * (i + 1)) for i in range(4)]

t = []
values = {sig: [] for sig in SIGNALS}
with CSV_PATH.open() as f:
    for row in csv.reader(f, delimiter=" "):
        fields = [x for x in row if x]
        if len(fields) < 2 * len(SIGNALS):
            continue
        t.append(float(fields[0]))
        for k, sig in enumerate(SIGNALS):
            values[sig].append(float(fields[2 * k + 1]))


def mean_current(current, t0, t1):
    vals = [c for tt, c in zip(t, current) if t0 <= tt <= t1]
    return sum(vals) / len(vals) if vals else float("nan")


r = {}
for i, row in enumerate(ROWS):
    _, t1 = READ_WINDOWS[i]
    for j, col in enumerate(COLS):
        i_mean = mean_current(values[f"i(vte{j+1})"], t1 - 0.125, t1)
        r[(row, col)] = VR / abs(i_mean)

labels = [f"({row[-1]},{col[-1]})\n" + ("written" if row == "BE1" and col == "TE1" else
          ("sneak-disturbed" if row == "BE1" or col == "TE1" else "untouched"))
          for row in ROWS for col in COLS]
for (row, col), value in r.items():
    print(f"R({row[-1]},{col[-1]}) = {value:.0f} ohm")

fig, axes = plt.subplots(3, 1, figsize=(10, 10), height_ratios=[1, 1, 1.2])

ax = axes[0]
colors_row = ["#c0392b", "#8e44ad", "#d35400", "#16a085"]
colors_col = ["#2e7d32", "#1565c0", "#f39c12", "#7f8c8d"]
for i, row in enumerate(ROWS):
    ax.plot(t, values[f"v({row.lower()})"], color=colors_row[i], linewidth=1.0, label=f"V({row})")
for j, col in enumerate(COLS):
    ax.plot(t, values[f"v({col.lower()})"], color=colors_col[j], linewidth=1.0, linestyle="--", label=f"V({col})")
ax.set_ylabel("Row/column voltage (V)")
ax.set_title("Real row/column drive -- write (1,1) only, then read rows 1-4 in turn")
ax.legend(fontsize=6, ncol=4, loc="upper right")

ax = axes[1]
for j, col in enumerate(COLS):
    ax.plot(t, [x * 1e3 for x in values[f"i(vte{j+1})"]], color=colors_col[j], linewidth=0.8, label=f"I({col})")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Column current (mA)")
ax.set_title("Real per-column current -- the write pulse, then all 4 real read windows")
ax.legend(fontsize=7, loc="upper right")

ax = axes[2]
bar_colors = ["#2e7d32" if "written" in l else "#c0392b" if "disturbed" in l else "#1565c0" for l in labels]
ax.bar(labels, [r[(row, col)] for row in ROWS for col in COLS], color=bar_colors)
ax.set_ylabel("Read resistance (ohm)")
ax.set_title("Real, computed per-cell read resistance -- 1 written, 6 sneak-disturbed, 9 untouched")
ax.tick_params(axis="x", labelsize=6)

fig.suptitle("4x4 Au/TiO2/Au memristor crossbar -- real ngspice/OSDI write-then-read (extracted-layout netlist)")
fig.tight_layout()
out_path = HERE / "crossbar4x4_write_read.png"
fig.savefig(out_path, dpi=150)
print(f"Wrote {out_path} from {len(t)} real, simulated data points.")
