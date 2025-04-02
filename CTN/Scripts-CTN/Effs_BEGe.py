##################################################################
## Script to determine HPGe mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

effs_22mm = [7.540e-2, 7.773e-2, 1.724e-2]

effs_20mm = [8.106e-2, 8.338e-2, 1.857e-2]

effs_mean, d_effs = np.zeros(3), np.zeros(3)

for k in range(3):
    effs_mean[k] = (effs_22mm[k] + effs_20mm[k])/2
    d_effs[k] = effs_mean[k] - effs_20mm[k]
    print(f"\t {effs_mean[k]:.5f} +- {d_effs[k]:.5f}")
