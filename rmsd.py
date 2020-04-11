import MDAnalysis as mda

universe = mda.Universe("1UBQ_solvate.psf", "1UBQ_eq.dcd")
print(universe)
print(len(universe.trajectory))
