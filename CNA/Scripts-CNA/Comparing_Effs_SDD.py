#################################################################
## Script to determine SDD mean efficiencies and uncertainties ##
#################################################################

## ---------------- ##
import numpy as np
## ---------------- ##

##  Efficiencies from simulation
                         # [   Ka   ,    Kb    , L- lines] 
effs_9mm_NoAl_SimNRA_Sn  = [[2.333e-03, 2.897e-04, 8.308e-04],
                            [2.335e-03, 2.873e-04, 8.323e-04],
                            [2.337e-03, 2.917e-04, 8.257e-04],
                            [2.337e-03, 2.882e-04, 8.400e-04],
                            [2.336e-03, 2.878e-04, 8.241e-04],
                            [2.338e-03, 2.907e-04, 8.188e-04]]

effs_9mm_NoAl_AEL_Sn =     [[2.341e-03, 2.903e-04, 8.393e-04],
                            [2.335e-03, 2.925e-04, 8.378e-04],
                            [2.338e-03, 2.906e-04, 8.275e-04],
                            [2.339e-03, 2.908e-04, 8.294e-04],
                            [2.341e-03, 2.886e-04, 7.980e-04],
                            [2.330e-03, 2.888e-04, 7.901e-04]]

effs_9mm_WithAl_AEL_Sn =   [[2.346e-03, 2.903e-04, 7.085e-04],
                            [2.332e-03, 2.901e-04, 7.142e-04],
                            [2.337e-03, 2.880e-04, 7.281e-04],
                            [2.332e-03, 2.894e-04, 8.281e-04],
                            [2.338e-03, 2.893e-04, 6.658e-04],
                            [2.330e-03, 2.883e-04, 7.002e-04]]

# Labels for each beam energy
beam_labels = ['Ebeam=3.2MeV', 'Ebeam=3.5MeV', 'Ebeam=3.9MeV',
               'Ebeam=4.3MeV', 'Ebeam=4.7MeV', 'Ebeam=5.0MeV']

effs_9mm_NoAl_SimNRA_Sn = np.array(effs_9mm_NoAl_SimNRA_Sn)
effs_9mm_NoAl_AEL_Sn = np.array(effs_9mm_NoAl_AEL_Sn)
effs_9mm_WithAl_AEL_Sn = np.array(effs_9mm_WithAl_AEL_Sn)

diffs = effs_9mm_NoAl_AEL_Sn - effs_9mm_WithAl_AEL_Sn
percent_diffsAl = 100 * (effs_9mm_NoAl_AEL_Sn - effs_9mm_WithAl_AEL_Sn) / effs_9mm_WithAl_AEL_Sn
percent_diffsSn = 100 * (effs_9mm_NoAl_SimNRA_Sn - effs_9mm_NoAl_AEL_Sn) / effs_9mm_NoAl_SimNRA_Sn


print("Percentual difference between efficiencies with and without Al thicknesses [(NoAl - WithAl)/WithAl * 100]:")
for i, label in enumerate(beam_labels):
    print(f"{label}: [Ka: {percent_diffsAl[i,0]:.2f}%, \t Kb: {percent_diffsAl[i,1]:.2f}%, \t L: {percent_diffsAl[i,2]:.2f}%]")

print()

print("Percentual difference between efficiencies from Sn thicknesses [(SimNRA - AEL)/SimNRA * 100]:")
for i, label in enumerate(beam_labels):
    print(f"{label}: [Ka: {percent_diffsSn[i,0]:.2f}%, \t Kb: {percent_diffsSn[i,1]:.2f}%, \t L: {percent_diffsSn[i,2]:.2f}%]")




