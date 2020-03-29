"""
This file extracts the energy levels given at each timestep in a NAMD log file
"""

import fileinput
from sys import stdout

import pandas as pd

energies_by_ts_and_type = []
energies_by_ts = []

for line in fileinput.input():
    if line.startswith("ENERGY:"):
        values = [m for m in [l.strip() for l in line.split(" ")][1:] if len(m) > 0]

        timestep = int(values[0])

        energies_by_ts.append({
            "timestep": timestep,
            "bond [kcal/mol]": float(values[1]),
            "angle [kcal/mol]": float(values[2]),
            "dihedral [kcal/mol]": float(values[3]),
            "improper [kcal/mol]": float(values[4]),
            "electrostatic [kcal/mol]": float(values[5]),
            "VDW [kcal/mol]": float(values[6])
        })

        columns = {}
        columns["bond"] = float(values[1])
        columns["angle"] = float(values[2])
        columns["dihedral"] = float(values[3])
        columns["improper"] = float(values[4])
        columns["electrostatic"] = float(values[5])
        columns["vdw"] = float(values[6])

        for energy, kcal_mol in columns.items():
            energies_by_ts_and_type.append({
                "timestep": timestep,
                "energy": energy,
                "kcal/mol": kcal_mol
            })

energies_by_ts_and_type_df = pd.DataFrame(energies_by_ts_and_type)
energies_by_ts_df = pd.DataFrame(energies_by_ts)

energies_by_ts_df.to_csv("energies_by_ts.csv", index=False)
energies_by_ts_and_type_df.to_csv("energies_by_ts_and_type.csv", index=True)
