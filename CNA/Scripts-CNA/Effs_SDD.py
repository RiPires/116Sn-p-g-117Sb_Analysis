#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

##  Efficiencies from simulation
          # [   Ka   ,    Kb    , L- lines] 
effs_9mm  = [[2.337e-3, 2.878e-4, 8.383e-4],
             [2.319e-3, 2.858e-4, 8.266e-4],
             [2.320e-3, 2.965e-4, 8.371e-4],
             [2.333e-3, 2.816e-4, 8.296e-4],
             [2.354e-3, 2.866e-4, 8.094e-4],
             [2.330e-3, 2.912e-4, 8.035e-4]]

effs_10mm = [[1.938e-03, 2.435e-04, 6.829e-04],
             [1.949e-03, 2.472e-04, 6.838e-04],
             [1.926e-03, 2.374e-04, 6.875e-04],
             [1.944e-03, 2.472e-04, 6.892e-04],
             [1.947e-03, 2.400e-04, 6.848e-04],
             [1.958e-03, 2.428e-04, 6.683e-04]]

effs_11mm = [[1.641e-03, 2.109e-04, 4.830e-04],
             [1.632e-03, 2.025e-04, 4.970e-04],
             [1.623e-03, 1.971e-04, 5.256e-04],
             [1.625e-03, 2.106e-04, 4.902e-04],
             [1.638e-03, 2.033e-04, 4.723e-04],
             [1.642e-03, 2.036e-04, 4.481e-04]]

effs_12mm = [[1.430e-3, 1.811e-4, 4.869e-4],
             [1.420e-3, 1.782e-4, 4.938e-4],
             [1.406e-3, 1.748e-4, 4.885e-4],
             [1.432e-3, 1.773e-4, 4.932e-4],
             [1.410e-3, 1.806e-4, 4.811e-4],
             [1.384e-3, 1.723e-4, 4.718e-4]]

# Labels for each beam energy
beam_labels = ['Ebeam=3.2MeV', 'Ebeam=3.5MeV', 'Ebeam=3.9MeV',
               'Ebeam=4.3MeV', 'Ebeam=4.7MeV', 'Ebeam=5.0MeV']

# Initialize result dictionary
efficiency_params = {}

for i, label in enumerate(beam_labels):
    effs_mean = [(effs_12mm[i][j] + effs_9mm[i][j]) / 2 for j in range(3)]
    d_effs = [abs(effs_mean[j] - effs_9mm[i][j]) for j in range(3)]
    
    efficiency_params[label] = {
        'Ka': (effs_mean[0], d_effs[0]), 'Kb': (effs_mean[1], d_effs[1]), 'L-': (effs_mean[2], d_effs[2])}

# Print dictionary
for label in beam_labels:
    ka_val, ka_err = efficiency_params[label]['Ka']
    kb_val, kb_err = efficiency_params[label]['Kb']
    l_val, l_err = efficiency_params[label]['L-']
    print(f"    '{label}': {{'Ka': ({ka_val:.3e}, {ka_err:.0e}), 'Kb': ({kb_val:.3e}, {kb_err:.0e}), 'L-': ({l_val:.3e}, {l_err:.0e})}},")