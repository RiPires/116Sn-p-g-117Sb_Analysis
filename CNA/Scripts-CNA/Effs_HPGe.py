##################################################################
## Script to determine HPGe mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

          #  [158 keV, Ka   , Kb    , 511 keV , 861 keV, 1004 keV]
effs_18mm = [[0.1171, 0.1230, 0.0266, 8.196e-4, 7.87e-5, 5.06e-5],
             [0.1171, 0.1228, 0.0266, 8.142e-4, 7.45e-5, 5.51e-5],
             [0.1171, 0.1226, 0.0265, 8.372e-4, 7.87e-5, 5.16e-5],
             [0.1172, 0.1227, 0.0266, 8.125e-4, 7.20e-5, 6.09e-5],
             [0.1172, 0.1228, 0.0265, 8.256e-4, 7.44e-5, 5.66e-5],
             [0.1171, 0.1228, 0.0265, 8.184e-4, 8.01e-5, 5.75e-5]]

effs_16mm = [[0.1271, 0.1310, 0.0284, 8.721e-4, 8.24e-5, 6.33e-5],
             [0.1272, 0.1309, 0.0283, 8.430e-4, 8.15e-5, 5.96e-5],
             [0.1269, 0.1308, 0.0284, 8.484e-4, 7.86e-5, 5.98e-5],
             [0.1273, 0.1309, 0.0283, 8.705e-4, 8.05e-5, 5.81e-5],
             [0.1272, 0.1310, 0.0285, 8.758e-4, 8.21e-5, 6.07e-5],
             [0.1270, 0.1309, 0.0284, 8.502e-4, 8.06e-5, 6.65e-5]]

# Labels for each beam energy
beam_labels = ['Ebeam=3.2MeV', 'Ebeam=3.5MeV', 'Ebeam=3.9MeV',
               'Ebeam=4.3MeV', 'Ebeam=4.7MeV', 'Ebeam=5.0MeV']

# Initialize result dictionary
efficiency_params = {}

for i, label in enumerate(beam_labels):
    effs_mean = [(effs_16mm[i][j] + effs_18mm[i][j]) / 2 for j in range(6)]
    d_effs = [abs(effs_mean[j] - effs_16mm[i][j]) for j in range(6)]
    
    efficiency_params[label] = {
        'gamma': (effs_mean[0], d_effs[0]), 'Ka': (effs_mean[1], d_effs[1]), 'Kb': (effs_mean[2], d_effs[2]), '511keV': (effs_mean[3], d_effs[3]), '861keV': (effs_mean[4], d_effs[4]), '1004keV': (effs_mean[5], d_effs[5])}

# Print dictionary
for label in beam_labels:
    gamma_val, gamma_err = efficiency_params[label]['gamma']
    ka_val, ka_err = efficiency_params[label]['Ka']
    kb_val, kb_err = efficiency_params[label]['Kb']
    val_511, err_511 = efficiency_params[label]['511keV']
    val_861, err_861 = efficiency_params[label]['861keV']
    val_1004, err_1004 = efficiency_params[label]['1004keV']
    print(f"    '{label}': {{'gamma': ({gamma_val:.3e}, {gamma_err:.0e}), 'Ka': ({ka_val:.3e}, {ka_err:.0e}), 'Kb': ({kb_val:.3e}, {kb_err:.0e}), '511keV': ({val_511:.3e}, {err_511:.0e}), '861keV': ({val_861:.3e}, {err_861:.0e}), '1004keV': ({val_1004:.3e}, {err_1004:.0e})}},")