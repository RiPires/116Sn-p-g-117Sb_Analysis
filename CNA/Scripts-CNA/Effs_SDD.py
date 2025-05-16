#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

##  Efficiencies from simulation
          # [   Ka   ,    Kb   ] 
effs_9mm  = [[2.337e-3, 2.878e-4],
             [2.319e-3, 2.858e-4],
             [2.320e-3, 2.965e-4],
             [2.333e-3, 2.816e-4],
             [2.354e-3, 2.866e-4],
             [2.330e-3, 2.912e-4]]

effs_12mm = [[1.430e-3, 1.811e-4],
             [1.420e-3, 1.782e-4],
             [1.406e-3, 1.748e-4],
             [1.432e-3, 1.773e-4],
             [1.410e-3, 1.806e-4],
             [1.384e-3, 1.723e-4]]

# Labels for each beam energy
beam_labels = ['Ebeam=3.2MeV', 'Ebeam=3.5MeV', 'Ebeam=3.9MeV',
               'Ebeam=4.3MeV', 'Ebeam=4.7MeV', 'Ebeam=5.0MeV']

# Initialize result dictionary
efficiency_params = {}

for i, label in enumerate(beam_labels):
    effs_mean = [(effs_9mm[i][j] + effs_12mm[i][j]) / 2 for j in range(2)]
    d_effs = [abs(effs_mean[j] - effs_9mm[i][j]) for j in range(2)]
    
    efficiency_params[label] = {
        'Ka': (effs_mean[0], d_effs[0]), 'Kb': (effs_mean[1], d_effs[1])}

# Print dictionary
for label in beam_labels:
    ka_val, ka_err = efficiency_params[label]['Ka']
    kb_val, kb_err = efficiency_params[label]['Kb']
    print(f"    '{label}': {{'Ka': ({ka_val:.3e}, {ka_err:.0e}), 'Kb': ({kb_val:.3e}, {kb_err:.0e})}},")