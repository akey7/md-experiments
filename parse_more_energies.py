import fileinput
import datetime

import pandas as pd

# The units for all these measures are from:
# http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node14.html#tab_namdstats

# An explanation for the units can be found at:
# https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-html/node27.html

# TS,BOND kcal/mol,ANGLE kcal/mol,DIHED kcal/mol,ANGLE kcal/mol,IMPRP kcal/mol,ELECT kcal/mol,VDW kcal/mol,BOUNDARY kcal/mol,MISC kcal/mol,KINETIC kcal/mol,TOTAL kcal/mol,TEMP K,     POTENTIAL kcal/mol,TOTAL3 kcal/mol,TEMPAVG K, PRESSURE bar, GPRESSURE bar, VOLUME Å^3, PRESSAVG bar,GPRESSAVG bar
# 0, 2060.4925,    1271.6255,     263.8635,      10.7301,        -19408.9902,  2463.6381,     0.0000,      0.0000,           0.0000,       -13338.6406,     0.0000,        -13338.6406,-13338.6406,       0.0000,         -311.4071, 3996.8932,    86856.0000,    -311.4071,  3996.8932

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
    "VOLUME Å^3",
    "PRESSAVG bar"
]

energies_and_temps_wide = []
energies_and_temps_tall = []

for line in fileinput.input():
    if line.startswith("ENERGY:"):
        values = [m for m in [l.strip() for l in line.strip().split(" ")][1:] if len(m) > 0]
        timestep = int(values[0])
        print(",".join(etitle))
        print(",".join(values))
        row = {}
        for i, key in enumerate(etitle):
            row[key] = values[i]
        energies_and_temps_wide.append(row)

wide_df = pd.DataFrame(energies_and_temps_wide)

timestamp = round(datetime.datetime.utcnow().timestamp())
wide_df.to_csv(f"namd_log_{timestamp}.csv", index=False)
