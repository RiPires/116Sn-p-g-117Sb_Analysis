######################################################
## Script for calculation of reaction cross-section ##
######################################################


## ---------------------------- ##
import numpy as np
from include.PlotData import*
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

# The number of radioactive nuclei at the end  of the irradiation, from the Npeak fit, 
# for each beam energy, and each radiation type, in the format [gamma, Ka, Kb]
""" N_D_irr1 = {
    "Ebeam=3.2MeV": {"gamma": 2.282e6, "Ka": 3.105e6, "Kb": 1.978e7},
    "Ebeam=3.5MeV": {"gamma": 9.036e6, "Ka": 1.236e7, "Kb": 7.791e7},
    "Ebeam=3.9MeV": {"gamma": 2.056e7, "Ka": 2.796e7, "Kb": 1.775e8},
    "Ebeam=4.3MeV": {"gamma": 3.999e7, "Ka": 5.444e7, "Kb": 3.456e8},
    "Ebeam=4.7MeV": {"gamma": 7.479e7, "Ka": 1.016e8, "Kb": 6.541e8},
    "Ebeam=5.0MeV": {"gamma": 1.495e8, "Ka": 1.992e8, "Kb": 1.291e9},} ## Using photopeak gaussian fit integration """

N_D_irr = {
    "Ebeam=3.2MeV": {"gamma": 2.300e6, "Ka": 3.197e6, "Kb": 2.033e7},
    "Ebeam=3.5MeV": {"gamma": 9.094e6, "Ka": 1.270e7, "Kb": 8.007e7},
    "Ebeam=3.9MeV": {"gamma": 2.070e7, "Ka": 2.875e7, "Kb": 1.827e8},
    "Ebeam=4.3MeV": {"gamma": 4.029e7, "Ka": 5.598e7, "Kb": 3.554e8},
    "Ebeam=4.7MeV": {"gamma": 7.539e7, "Ka": 1.044e8, "Kb": 6.734e8},
    "Ebeam=5.0MeV": {"gamma": 1.509e8, "Ka": 2.046e8, "Kb": 1.329e9},} ## Using photopeak channel by channel yield sum

## 3   - Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
##       t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant)

## RBS detector efficiency
epsilon_p = 4.409e-4

## Tin 116 atomic weight enrichment
wA = 0.978

## 117Sb decay half-life in minutes (2.8 hours)
halfLife_min = 2.8*60 # minutes
decayConstant = np.log(2) / halfLife_min  # in min^-1

## Total irradiation time, in minutes, for each activation
t_irr_min = {"Ebeam=3.2MeV": 358,
             "Ebeam=3.5MeV": 365,  
             "Ebeam=3.9MeV": 360,
             "Ebeam=4.3MeV": 361,
             "Ebeam=4.7MeV": 347,
             "Ebeam=5.0MeV": 344,}

## Total number of backscattered protons, Np
N_p = {
    "Ebeam=3.2MeV": 8.41e7,
    "Ebeam=3.5MeV": 1.03e8,
    "Ebeam=3.9MeV": 5.90e7,
    "Ebeam=4.3MeV": 4.87e7,
    "Ebeam=4.7MeV": 2.64e7,
    "Ebeam=5.0MeV": 2.64e7,
}

## ---------------- Cross-Section Calculation ---------------- ##
crossSections = {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    print(f"Cross-section for {key}")

    if key in N_D_irr:
        t_irr = t_irr_min[key]  # irradiation time
        Np = N_p[key]  # incident protons
        
        # Compute the decay factor
        decayFactor = 1 - np.exp(-decayConstant * t_irr)
        
        # Compute the cross-section for each radiation type
        crossSections[key] = {}
        for rad_type, N_D in N_D_irr[key].items():
            sigma = (
                ruthCrossSection[i] *
                (4 * np.pi * N_D * epsilon_p) /
                (decayFactor) *
                (decayConstant * t_irr / (wA * Np))
            )
            
            # Store result
            crossSections[key][rad_type] = sigma
            print(f"{rad_type}: {sigma:.4e} mb")

    print()
    
PlotCrossSection(crossSections)