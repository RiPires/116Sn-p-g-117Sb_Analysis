#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

effs_9mm = [2.325e-04, 2.989e-05, 6.173e-05]

effs_11mm = [1.649e-04, 1.972e-05, 4.474e-05]

effs_14mm = [1.053e-03, 1.355e-04, 2.781e-05]

effs_16mm = [8.296e-04, 1.032e-04, 2.131e-05]


effs_mean, d_effs = np.zeros(3), np.zeros(3)

for k in range(3):
    effs_mean[k] = (effs_16mm[k] + effs_14mm[k])/2
    d_effs[k] = effs_mean[k] - effs_14mm[k]
    print(f"\t {effs_mean[k]:.3e} +- {d_effs[k]:.0e}")
