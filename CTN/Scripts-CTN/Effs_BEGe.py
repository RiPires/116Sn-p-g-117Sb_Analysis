##################################################################
## Script to determine BPGe mean efficiencies and uncertainties ##
##################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

effs_27mm = [6.743e-2, 7.210e-2, 1.599e-2]

effs_25mm = [7.250e-2, 7.738e-2, 1.712e-2]

effs_22mm = [8.073e-2, 8.655e-2, 1.922e-2]

effs_20mm = [8.696e-2, 9.273e-2, 2.072e-2]

effs_mean, d_effs = np.zeros(3), np.zeros(3)

for k in range(3):
    effs_mean[k] = (effs_27mm[k] + effs_25mm[k])/2
    d_effs[k] = effs_mean[k] - effs_25mm[k]
    print(f"\t {effs_mean[k]:.5f} +- {d_effs[k]:.5f}")
