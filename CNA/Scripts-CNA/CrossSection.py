######################################################
## Script for calculation of reaction cross-section ##
######################################################


## ---------------------------- ##
import numpy as np
## ---------------------------- ##

## ____________ Constants ____________ ##
zBeam = 1
zTarget = 50
eCharge = 1.60217663e-19 # C
epsilon0 = 8.8541878e-12 # F/m
scattAngDeg = 165 # deg
scattAngRad = np.deg2rad(scattAngDeg) # radians
cSpeed = 2.99792458e8 # m/s
## ___________________________________ ## 

## *********************************************************************** ## 
## Will start with the cross-section calculation using the relative method ##
## *********************************************************************** ##

## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ##
## 1   - Calculate the Rutherford diff. cross-section for each beam energy;
## 2   - Determine the total number of radioactive nuclei in the target at the end of the irradiation,
##       N_Dirr, from the fit of Npeak, for each radiation type (gamma, Ka and Kb);
## 2.1 - For the Npeak fit, use the values of epsilonD (SDD and HPGe detectors resolution) extracted from the Geant4 simulation,
##       the eta (decay branching ratio) from literature, t_trans (transportation time of the target from irradiation chamber to decay station)
##       as measured during the experiment, as well as the acquisition time (tacqui);
## 3   - Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
##       t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant);
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ##

## 1 - Calculate Rutherford Differential Cross-Section
energies = np.array([3.2, 3.5, 3.9, 4.3, 4.7, 5.0]) # MeV
ruthCrossSection = ( (zBeam*zTarget*eCharge) / (16*np.pi*epsilon0*energies*10**6*np.sin(scattAngRad/2)**2) )**2 *1e31 # mb/sr

print(ruthCrossSection)

## 2 - Determine the total number of radioactive nuclei in the target at the end of the irradiation,
##     N_Dirr, from the fit of Npeak, for each radiation type (gamma, Ka and Kb);

