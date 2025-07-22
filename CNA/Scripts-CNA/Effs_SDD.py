#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

##  Efficiencies from simulation
          # [   Ka   ,    Kb    , L- lines] 
effs_9mm  = [[2.335e-03, 2.883e-04, 7.638e-04],
             [2.334e-03, 2.863e-04, 7.713e-04],
             [2.345e-03, 2.937e-04, 7.712e-04],
             [2.342e-03, 2.885e-04, 7.670e-04],
             [2.339e-03, 2.902e-04, 7.471e-04],
             [2.332e-03, 2.908e-04, 7.295e-04]]

effs_10mm = [[1.938e-03, 2.440e-04, 6.302e-04],
             [1.948e-03, 2.424e-04, 6.387e-04],
             [1.947e-03, 2.415e-04, 6.396e-04],
             [1.952e-03, 2.403e-04, 6.377e-04],
             [1.947e-03, 2.433e-04, 6.150e-04],
             [1.947e-03, 2.420e-04, 6.014e-04]]

effs_11mm = [[1.641e-03, 2.109e-04, 4.830e-04],
             [1.632e-03, 2.025e-04, 4.970e-04],
             [1.623e-03, 1.971e-04, 5.256e-04],
             [1.625e-03, 2.106e-04, 4.902e-04],
             [1.638e-03, 2.033e-04, 4.723e-04],
             [1.642e-03, 2.036e-04, 4.481e-04]]

effs_12mm = [[1.411e-03, 1.750e-04, 4.493e-04],
             [1.413e-03, 1.767e-04, 4.505e-04],
             [1.410e-03, 1.733e-04, 4.577e-04],
             [1.413e-03, 1.758e-04, 4.518e-04],
             [1.411e-03, 1.756e-04, 4.404e-04],
             [1.411e-03, 1.747e-04, 4.302e-04]]

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