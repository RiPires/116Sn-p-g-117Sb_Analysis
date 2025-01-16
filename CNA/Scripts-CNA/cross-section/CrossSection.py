######################################################
## Script for calculation of reaction cross-section ##
######################################################


## ---------------------------- ##

## ---------------------------- ##

## *********************************************************************** ## 
## Will start with the cross-section calculation using the relative method ##
## *********************************************************************** ##

## 1   - Calculate the Rutherford diff cross-section for each beam energy;
## 2   - Determine the total number of radioactive nuclei in the target at the end of the irradiation,
##       N_Dirr, from the fit of Npeak, for each radiation type (gamma, Ka and Kb);
## 2.1 - For the Npeak fit, use the values of epsilonD (SDD and HPGe detectors resolution) extracted from the Geant4 simulation,
##       the eta (decay branching ratio) from literature, t_trans (transportation time of the target from irradiation chamber to decay station)
##       as measured during the experiment, as well as the acquisition time (tacqui);
## 3   - Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
##       t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant);