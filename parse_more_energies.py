import fileinput
import datetime

import pandas as pd

# The units for all these measures are from:
# http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node14.html#tab_namdstats

# An explanation for the units can be found at:
# https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-html/node27.html

# These aren't all the values...they are the values that are I found on every line of
# the log file.

etitle = [
    "TS",
    "BOND kcal/mol",
    "ANGLE kcal/mol",
    "DIHED kcal/mol",
    "ANGLE kcal/mol",
    "IMPRP kcal/mol",
    "ELECT kcal/mol",
    "VDW kcal/mol",
    "BOUNDARY kcal/mol",
    "MISC kcal/mol",
    "KINETIC kcal/mol",
    "TOTAL kcal/mol",
    "TEMP K",
    "POTENTIAL kcal/mol",
    "TOTAL3 kcal/mol",
    "TEMPAVG K",
    "PRESSURE bar",
    "GPRESSURE bar",
    "VOLUME Å^3"
]

energies_and_temps_wide = []
energies_and_temps_tall = []

for line in fileinput.input():
    if line.startswith("ENERGY:"):
        values = [m for m in [l.strip() for l in line.strip().split(" ")][1:] if len(m) > 0]
        row = {}
        for i, key in enumerate(etitle):
            row[key] = float(values[i])
        energies_and_temps_wide.append(row)
        for key, value in row.items():
            if key != "TS":
                energies_and_temps_tall.append({
                    "timestep": int(values[0]),
                    key: value
                })

wide_df = pd.DataFrame(energies_and_temps_wide)
tall_df = pd.DataFrame(energies_and_temps_tall)

timestamp = round(datetime.datetime.utcnow().timestamp())
wide_df.to_csv(f"namd_log_{timestamp}.wide.csv", index=False)
tall_df.to_csv(f"namd_log_{timestamp}.tall.csv", index=True)
