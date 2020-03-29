"""
This file extracts the energy levels given at each timestep in a NAMD log file
"""

import fileinput
from sys import stdout

import pandas as pd

# TS           BOND          ANGLE          DIHED          IMPRP               ELECT            VDW

rows = []
for line in fileinput.input():
    if line.startswith("ENERGY:"):
        values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]
        row = {
            "timestep": int(values[0]),
            "bond [kcal / mol]": float(values[1]),
            "angle [kcal / mol]": float(values[2]),
            "dihedral [kcal / mol]": float(values[3]),
            "improper [kcal / mol]": float(values[4]),
            "electrostatic [kcal / mol]": float(values[5]),
            "VDW [kcal / mol]": float(values[6])
        }
        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(stdout, index=False)