#!/usr/bin/env python3
"""report.py -- the main results of the last LibreLane run, in plain
words. LibreLane keeps them all in runs/<run>/final/metrics.json."""
import glob
import json
import os

runs = sorted(glob.glob("runs/*/final/metrics.json"), key=os.path.getmtime)
if not runs:
    raise SystemExit("No layout yet: run 'make layout' first.")
m = json.load(open(runs[-1]))


def check(n):
    return "OK (0 problems)" if n == 0 else f"{n} PROBLEMS"


die = m["design__die__area"]
drc = m["magic__drc_error__count"] + m["klayout__drc_error__count"] + m["route__drc_errors"]
setup = m["timing__setup__ws"]
hold = m["timing__hold__ws"]
print(f"Run                 {runs[-1].split('/')[1]}")
print(f"Chip size           {die:.0f} um2, about {die ** 0.5:.0f} x {die ** 0.5:.0f} um")
print(f"Cells placed        {m['design__instance__count__stdcell']}")
print(f"Wires               {m['route__wirelength']:.0f} um in total")
print(f"Design rules (DRC)  {check(drc)}")
print(f"Layout vs. netlist  {check(m['design__lvs_error__count'])}")
print(f"Antennas            {check(m['route__antenna_violation__count'])}")
print(f"Timing, 10 ns clock {'OK' if setup >= 0 and hold >= 0 else 'TOO SLOW'}"
      f" ({setup:.1f} ns to spare in the slowest corner)")
