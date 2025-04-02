#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

effs_9mm = [[2.327e-3, 3.082e-4],
            [2.344e-3, 2.979e-4],
            [2.322e-3, 2.993e-4],
            [2.345e-3, 2.988e-4],
            [2.329e-3, 2.896e-4],
            [2.345e-3, 2.994e-4]]

effs_12mm = [[1.404e-3, 1.862e-4],
             [1.409e-3, 1.760e-4],
             [1.413e-3, 1.801e-4],
             [1.400e-3, 1.801e-4],
             [1.409e-3, 1.836e-4],
             [1.436e-3, 1.848e-4]]

effs_mean, d_effs = np.zeros(shape=(6,2)), np.zeros(shape=(6,2))

for i in range(6):
    for k in range(2):
        effs_mean[i][k] = (effs_9mm[i][k] + effs_12mm[i][k])/2
        d_effs[i][k] = effs_mean[i][k] - effs_9mm[i][k]
        print(f"\t {effs_mean[i][k]:.3e} +- {d_effs[i][k]:.0e}")
    print()