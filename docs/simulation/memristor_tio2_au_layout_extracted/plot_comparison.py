"""Plots a real, direct comparison between the original hand-written
testbench's own real ngspice/OSDI transient (../memristor_tio2_au/
memristor_tran.csv) and this directory's own real transient, driven
through the real, Magic-extracted memristor_tio2_au layout netlist
(memristor_extracted_tran.csv) instead of a bare model/instance line.
Reads real, already-simulated data only; never runs ngspice itself."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent


def read_csv(path):
    t, v, i = [], [], []
    with path.open() as f:
        for row in csv.reader(f, delimiter=" "):
            fields = [x for x in row if x]
            if len(fields) < 4:
                continue
            t.append(float(fields[0]))
            v.append(float(fields[1]))
            i.append(float(fields[3]))
    return t, v, i

t_orig, v_orig, i_orig = read_csv(HERE.parent / "memristor_tio2_au" / "memristor_tran.csv")
t_ext, v_ext, i_ext = read_csv(HERE / "memristor_extracted_tran.csv")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
ax.plot([x * 1e3 for x in i_orig], v_orig, color="#999999", linewidth=3.0,
        label="Original hand-written testbench")
ax.plot([x * 1e3 for x in i_ext], v_ext, color="#c0392b", linewidth=1.2,
        linestyle="--", label="Through the real extracted layout netlist")
ax.axhline(0, color="#cccccc", linewidth=0.6)
ax.axvline(0, color="#cccccc", linewidth=0.6)
ax.set_xlabel("Current through memristor (mA)")
ax.set_ylabel("Voltage across memristor (V)")
ax.set_title("Pinched I-V hysteresis loop -- overlay")
ax.legend(fontsize=8)

max_abs_i = max(abs(x) for x in i_orig)
diff = [(a - b) / max_abs_i * 100 for a, b in zip(i_orig, i_ext)]
ax = axes[1]
ax.plot(t_ext, diff, color="#1565c0", linewidth=1.0)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current difference (% of peak I)")
ax.set_title("Original vs. extracted-netlist current -- relative error")

fig.suptitle("memristor_tio2_au -- original testbench vs. real, Magic-extracted layout netlist")
fig.tight_layout()
out_path = HERE / "comparison.png"
fig.savefig(out_path, dpi=150)
max_diff = max(abs(x) for x in diff)
print(f"Wrote {out_path}. Max relative current difference: {max_diff:.4f}% of peak.")
