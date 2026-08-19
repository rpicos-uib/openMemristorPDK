"""Plots the real ngspice transient output (memristor_tran.csv) for
the Au/TiO2/Ti device variant -- the classic memristor fingerprint (a
pinched I-V hysteresis loop) plus the raw V(t)/I(t) waveforms that
produced it. Reads real, already-simulated data only; never runs
ngspice itself."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).parent
CSV_PATH = HERE / "memristor_tran.csv"

t, v, i = [], [], []
with CSV_PATH.open() as f:
    for row in csv.reader(f, delimiter=" "):
        fields = [x for x in row if x]
        if len(fields) < 4:
            continue
        t.append(float(fields[0]))
        v.append(float(fields[1]))
        i.append(float(fields[3]))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
ax.plot([x * 1e3 for x in i], v, color="#c0392b", linewidth=1.4)
ax.axhline(0, color="#999999", linewidth=0.6)
ax.axvline(0, color="#999999", linewidth=0.6)
ax.set_xlabel("Current through memristor (mA)")
ax.set_ylabel("Voltage across memristor (V)")
ax.set_title("Pinched I-V hysteresis loop\n(real ngspice/OSDI transient, memristor_tio2_ti.va)")

ax = axes[1]
ax.plot(t, v, color="#2e7d32", linewidth=1.2, label="V(TE) [V]")
ax2 = ax.twinx()
ax2.plot(t, [x * 1e3 for x in i], color="#1565c0", linewidth=1.0, label="I [mA]")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)", color="#2e7d32")
ax2.set_ylabel("Current (mA)", color="#1565c0")
ax.set_title("Au/TiO2/Ti -- V(t)/I(t)")

fig.suptitle("Au/TiO2/Ti memristor -- real ngspice/OSDI transient")
fig.tight_layout()
out_path = HERE / "memristor_transient.png"
fig.savefig(out_path, dpi=150)
print(f"Wrote {out_path} from {len(t)} real, simulated data points.")
