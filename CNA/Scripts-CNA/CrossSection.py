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
scattAngDeg_err = 2.3 # deg
scattAngRad = np.deg2rad(scattAngDeg) # radians
scattAngRad_err = np.deg2rad(scattAngDeg_err) # radians
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
#print(ruthCrossSection)

## Compute Ruth cross-section error
alfa = ((zBeam*zTarget*eCharge)/(16*np.pi*epsilon0*10**6))**2 * 10**31
ruthCrossSection_err = (alfa * np.cos(scattAngRad/2))/(energies * (np.sin(scattAngRad/2))**3) * scattAngRad_err ## mbarn
#print(ruthCrossSection_err)


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

N_D_irr_HPGe = {
    "Ebeam=3.2MeV": {"gamma": 2.318e6, "Ka": 3.223e6, "Kb": 2.049e7},
    "Ebeam=3.5MeV": {"gamma": 9.171e6, "Ka": 1.281e7, "Kb": 8.075e7},
    "Ebeam=3.9MeV": {"gamma": 2.088e7, "Ka": 2.901e7, "Kb": 1.843e8},
    "Ebeam=4.3MeV": {"gamma": 4.069e7, "Ka": 5.654e7, "Kb": 3.589e8},
    "Ebeam=4.7MeV": {"gamma": 7.565e7, "Ka": 1.048e8, "Kb": 6.756e8},
    "Ebeam=5.0MeV": {"gamma": 1.521e8, "Ka": 2.063e8, "Kb": 1.340e9},} ## Using photopeak channel by channel yield sum

N_D_irr_SDD = {
                      "Ebeam=3.2MeV": {"Ka": 2.658e6, "Kb": 1.267e7},
                      "Ebeam=3.5MeV": {"Ka": 1.062e7, "Kb": 5.441e7},
                      "Ebeam=3.9MeV": {"Ka": 2.585e7, "Kb": 1.265e8},
                      "Ebeam=4.3MeV": {"Ka": 5.020e7, "Kb": 2.591e8},
                      "Ebeam=4.7MeV": {"Ka": 1.052e8, "Kb": 4.834e8},
                      "Ebeam=5.0MeV": {"Ka": 2.114e8, "Kb": 1.014e9},} ## Using photopeak channel by channel yield sum

## Error values of N_Dirr from the fit
N_D_irr_HPGe_err = {
    "Ebeam=3.2MeV": {"gamma": 4e2, "Ka": 9e2, "Kb": 1e4},
    "Ebeam=3.5MeV": {"gamma": 3e3, "Ka": 3e3, "Kb": 3e4},
    "Ebeam=3.9MeV": {"gamma": 9e3, "Ka": 6e3, "Kb": 7e4},
    "Ebeam=4.3MeV": {"gamma": 2e4, "Ka": 1e4, "Kb": 1e5},
    "Ebeam=4.7MeV": {"gamma": 2e4, "Ka": 2e4, "Kb": 1e5},
    "Ebeam=5.0MeV": {"gamma": 6e4, "Ka": 3e4, "Kb": 5e5},} ## Using photopeak channel by channel yield sum

N_D_irr_SDD_err = {
    "Ebeam=3.2MeV": {"Ka": 2e3, "Kb": 4e4},
    "Ebeam=3.5MeV": {"Ka": 1e4, "Kb": 6e4},
    "Ebeam=3.9MeV": {"Ka": 2e4, "Kb": 2e5},
    "Ebeam=4.3MeV": {"Ka": 4e4, "Kb": 2e5},
    "Ebeam=4.7MeV": {"Ka": 4e4, "Kb": 2e5},
    "Ebeam=5.0MeV": {"Ka": 9e4, "Kb": 4e5},} ## Using photopeak channel by channel yield sum

## 3   - Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
##       t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant)

## RBS detector efficiency
epsilon_p = 4.409e-4

## Tin 116 atomic weight enrichment
wA = 0.978

## 117Sb decay half-life in minutes (2.8 hours)
halfLife_min = 2.8*60 # minutes
halfLife_min_err = 0.01*60 # minutes

## Decay constant
decayConstant = np.log(2) / halfLife_min  # in min^-1
decayConstant_err = np.log(2) * halfLife_min_err / halfLife_min**2  # in min^-1

## Total irradiation time, in minutes, for each activation
t_irr_min = {"Ebeam=3.2MeV": 358,
             "Ebeam=3.5MeV": 365,  
             "Ebeam=3.9MeV": 360,
             "Ebeam=4.3MeV": 361,
             "Ebeam=4.7MeV": 347,
             "Ebeam=5.0MeV": 344,}
t_irr_err = 1. # minute

## Total number of backscattered protons, Np
N_p = {"Ebeam=3.2MeV": 8.41e7,
       "Ebeam=3.5MeV": 1.03e8,
       "Ebeam=3.9MeV": 5.90e7,
       "Ebeam=4.3MeV": 4.87e7,
       "Ebeam=4.7MeV": 2.64e7,
       "Ebeam=5.0MeV": 2.64e7,}

## ---------------- Cross-Section Calculation ---------------- ##
crossSections_HPGe = {}
crossSections_HPGe_err = {}
crossSections_SDD = {}
crossSections_SDD_err = {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    print(f"HPGe Cross-section for {key}")

    if key in N_D_irr_HPGe:
        t_irr = t_irr_min[key]  # irradiation time
        Np = N_p[key]           # incident protons
        
        # Compute the decay factor
        decayFactor = 1 - np.exp(-decayConstant * t_irr)
        
        # Compute the cross-section for each radiation type
        crossSections_HPGe[key] = {}
        crossSections_HPGe_err[key] = {}

        for rad_type, N_D in N_D_irr_HPGe[key].items():

            ## Get N_D_irr errors
            N_D_err = N_D_irr_HPGe_err[key][rad_type]
            
            ## Cross-Section calculation
            sigma = (ruthCrossSection[i] *
                (4 * np.pi * N_D * epsilon_p) / (decayFactor) *
                (decayConstant * t_irr / (wA * Np)))
            
            ## Compute error propagation
            sigma_err = np.sqrt(sigma**2/Np + 
                                (sigma*ruthCrossSection_err[i]/ruthCrossSection[i])**2 +
                                (sigma/N_D)**2 * N_D_err**2 + 
                                ((decayConstant*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np*wA))**2 * t_irr_err**2 + 
                                ((t_irr*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np*wA))**2 * decayConstant_err**2)
            
            ## Store the results
            crossSections_HPGe[key][rad_type] = sigma
            crossSections_HPGe_err[key][rad_type] = sigma_err

            print(f"{rad_type}: ({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    print(f"SDD Cross-section for {key}")

    if key in N_D_irr_SDD:
        t_irr = t_irr_min[key]  # irradiation time
        Np = N_p[key]  # incident protons
        
        # Compute the decay factor
        decayFactor = 1 - np.exp(-decayConstant * t_irr)
        
        # Compute the cross-section for each radiation type
        crossSections_SDD[key] = {}
        crossSections_SDD_err[key] = {}

        for rad_type, N_D in N_D_irr_SDD[key].items():

            ## Get N_D_irr errors
            N_D_err = N_D_irr_SDD_err[key][rad_type]

            ## Cross-Section calculation
            sigma = (ruthCrossSection[i] *
                (4 * np.pi * N_D * epsilon_p) / (decayFactor) *
                (decayConstant * t_irr / (wA * Np)))
            
                        ## Compute error propagation
            sigma_err = np.sqrt(sigma**2/Np + 
                                (sigma/N_D)**2 * N_D_err**2 + 
                                ((decayConstant*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np*wA))**2 * t_irr_err**2 + 
                                ((t_irr*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np*wA))**2 * decayConstant_err**2)
            
            # Store result
            crossSections_SDD[key][rad_type] = sigma
            crossSections_SDD_err[key][rad_type] = sigma_err

            print(f"{rad_type}: ({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err)