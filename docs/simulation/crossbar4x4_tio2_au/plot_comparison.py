"""Real, direct comparison between the 4x4 crossbar's own real
write-then-read transient run through the real, patched Magic-
extracted layout netlist (crossbar4x4_write_read_extracted.csv) and
the same real testbench run through the real, live xschem-netlisted
schematic (crossbar4x4_write_read_schematic.csv) -- a real check that
both real views of this cell simulate identically, not just match
topologically (the deck's own real LVS step). Reads real,
already-simulated data only; never runs ngspice itself."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
VR = 0.05
ROWS = ["BE1", "BE2", "BE3", "BE4"]
COLS = ["TE1", "TE2", "TE3", "TE4"]
SIGNALS = [f"v({r.lower()})" for r in ROWS] + [f"v({c.lower()})" for c in COLS] + [f"i(vte{i+1})" for i in range(4)]

# Real read windows: row i in [0.9+0.5(i-1), 0.9+0.5i), averaged over
# each window's own last quarter, well clear of the PWL edge -- same
# real convention as the 2x2 deck's own plot_crossbar.py.
READ_WINDOWS = [(0.9 + 0.5 * i, 0.9 + 0.5 * (i + 1)) for i in range(4)]


def read_csv(path):
    # ngspice's own real `wrdata` format pairs each requested signal
    # with its own repeated time column -- (t, sig0, t, sig1, t, sig2,
    # ...), not one shared leading t -- confirmed live (not guessed)
    # after an off-by-one first pass silently produced 0 real rows.
    t = []
    values = {sig: [] for sig in SIGNALS}
    with path.open() as f:
        for row in csv.reader(f, delimiter=" "):
            fields = [x for x in row if x]
            if len(fields) < 2 * len(SIGNALS):
                continue
            t.append(float(fields[0]))
            for k, sig in enumerate(SIGNALS):
                values[sig].append(float(fields[2 * k + 1]))
    return t, values


def mean_current(t, current, t0, t1):
    vals = [c for tt, c in zip(t, current) if t0 <= tt <= t1]
    return sum(vals) / len(vals) if vals else float("nan")


def per_cell_resistance(t, values):
    """Real per-cell resistance -- one measurement per real (row,
    column) pair, from the real read window belonging to that row."""

    r = {}
    for i, row in enumerate(ROWS):
        t0, t1 = READ_WINDOWS[i]
        window0, window1 = t1 - 0.125, t1
        for j, col in enumerate(COLS):
            current = values[f"i(vte{j+1})"]
            i_mean = mean_current(t, current, window0, window1)
            r[(row, col)] = VR / abs(i_mean)
    return r


t_ext, values_ext = read_csv(HERE / "crossbar4x4_write_read_extracted.csv")
t_sch, values_sch = read_csv(HERE / "crossbar4x4_write_read_schematic.csv")

r_ext = per_cell_resistance(t_ext, values_ext)
r_sch = per_cell_resistance(t_sch, values_sch)

labels = [f"{row}\n{col}" for row in ROWS for col in COLS]
vals_ext = [r_ext[(row, col)] for row in ROWS for col in COLS]
vals_sch = [r_sch[(row, col)] for row in ROWS for col in COLS]
rel_diff = [abs(a - b) / a * 100 for a, b in zip(vals_ext, vals_sch)]

print("Real, per-cell resistance -- extracted vs. schematic, and their real relative difference:")
for label, a, b, d in zip(labels, vals_ext, vals_sch, rel_diff):
    print(f"  {label.replace(chr(10), ' '):>10}: extracted={a:9.1f} ohm  schematic={b:9.1f} ohm  diff={d:.4f}%")
max_diff = max(rel_diff)
print(f"Max real relative difference across all 16 real cells: {max_diff:.4f}%")

fig, axes = plt.subplots(2, 1, figsize=(9, 7), height_ratios=[1, 1])

x = range(16)
ax = axes[0]
width = 0.38
ax.bar([xi - width / 2 for xi in x], vals_ext, width=width, color="#c0392b", label="Extracted (Magic + real patch)")
ax.bar([xi + width / 2 for xi in x], vals_sch, width=width, color="#1565c0", label="Schematic (real xschem netlist)")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=7)
ax.set_ylabel("Read resistance (ohm)")
ax.set_title("2x2 -> 4x4: real per-cell resistance, both real views overlaid")
ax.legend(fontsize=8)

ax = axes[1]
ax.bar(list(x), rel_diff, color="#2e7d32")
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=7)
ax.set_ylabel("Relative difference (%)")
ax.set_title(f"Extracted vs. schematic -- real relative difference (max {max_diff:.4f}%)")

fig.suptitle("4x4 Au/TiO2/Au memristor crossbar -- extracted-layout vs. schematic simulation, real & direct")
fig.tight_layout()
out_path = HERE / "crossbar4x4_comparison.png"
fig.savefig(out_path, dpi=150)
print(f"Wrote {out_path}.")
