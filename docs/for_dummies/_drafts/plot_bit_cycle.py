import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
d = np.loadtxt("bit.csv")
t, v, i = d[:,0]*1e9, d[:,1], d[:,3]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True, dpi=130)
a1.plot(t, v, color="#2b6cb0", lw=2); a1.set_ylabel("Voltage (V)"); a1.axhline(0, color="#999", lw=0.6)
a1.axhline(0.8, color="#c53030", lw=0.8, ls="--"); a1.axhline(-0.6, color="#c53030", lw=0.8, ls="--")
a1.text(497, 0.83, "SET threshold +0.8 V", ha="right", fontsize=8, color="#c53030")
a1.text(497, -0.57, "RESET threshold -0.6 V", ha="right", fontsize=8, color="#c53030")
for x, lab in ((50, "read"), (150, "write 1"), (250, "read"), (350, "write 0"), (450, "read")):
    a1.text(x, 1.32, lab, ha="center", fontsize=9, fontweight="bold")
a1.set_ylim(-1.3, 1.55)
a2.semilogy(t, np.maximum(np.abs(i), 1e-2), color="#2f855a", lw=2); a2.set_ylabel("|Current| (µA)")
for x, y, lab in ((60, 4, "4 µA → bit 0"), (260, 400, "400 µA → bit 1"), (460, 4, "4 µA → bit 0")):
    a2.annotate(lab, (x, y), xytext=(x, y*6 if y < 100 else y/12), ha="center", fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
a2.set_xlabel("Time (ns)"); a2.set_ylim(0.05, 1e5)
for a in (a1, a2):
    for x in (100, 200, 300, 400): a.axvline(x, color="#ddd", lw=0.8, zorder=0)
fig.suptitle("One Au/HfO₂/Al memristor storing one bit (ngspice + OpenVAF)", fontsize=11)
fig.tight_layout(); fig.savefig("g01_bit_cycle.png")
