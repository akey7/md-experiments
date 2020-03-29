"""
This file extracts the energy levels given at each timestep in a NAMD log file
"""

import fileinput
import datetime

import pandas as pd

wide = []
tall = []

for line in fileinput.input():
    if line.startswith("ENERGY:"):
        values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]

        timestep = int(values[0])

        wide_row = {
            "timestep": timestep,
            "bond [kcal/mol]": float(values[1]),
            "angle [kcal/mol]": float(values[2]),
            "dihedral [kcal/mol]": float(values[3]),
            "improper [kcal/mol]": float(values[4]),
            "electrostatic [kcal/mol]": float(values[5]),
            "VDW [kcal/mol]": float(values[6]),
            "temp [K]": float(values[11])
        }

        wide.append(wide_row)

        for key, value in wide_row.items():
            if key != "timestep":
                tall_row = {
                    "timestep": timestep,
                    "measurement": key,
                    "value": value
                }
                tall.append(tall_row)

write_timestamp = round(datetime.datetime.utcnow().timestamp())

wide_df = pd.DataFrame(wide)
wide_df.to_csv(f"energies_wide.{write_timestamp}.csv", index=True, index_label="index")

tall_df = pd.DataFrame(tall)
tall_df.to_csv(f"energies_tall.{write_timestamp}.csv", index=True, index_label="index")
