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
scattAngDeg_CTN = 155 # deg
scattAngDeg_err = 2.3 # deg
scattAngDeg_CTN_err = 2. # deg # VERIFICAR ESTE VALOR !!!
scattAngRad = np.deg2rad(scattAngDeg) # radians
scattAng_CTN_Rad = np.deg2rad(scattAngDeg_CTN) # radians
scattAngRad_err = np.deg2rad(scattAngDeg_err) # radians
scattAngRad_CTN_err = np.deg2rad(scattAngDeg_CTN_err) # radians
cSpeed = 2.99792458e8 # m/s
## ___________________________________ ## 


## Calculate Rutherford Differential Cross-Section
energies = np.array([3.2, 3.5, 3.9, 4.3, 4.7, 5.0]) # MeV
ruthCrossSection = ( (zBeam*zTarget*eCharge) / (16*np.pi*epsilon0*energies*10**6*np.sin(scattAngRad/2)**2) )**2 *1e31 # mb/sr
ruthCrossSection_CTN = ( (zBeam*zTarget*eCharge) / (16*np.pi*epsilon0*3.215*10**6*np.sin(scattAng_CTN_Rad/2)**2) )**2 *1e31

## Compute error propagation
#alfa = ((zBeam*zTarget*eCharge)/(16*np.pi*epsilon0*10**6))**2 * 10**31
#ruthCrossSection_err = (alfa * np.cos(scattAngRad/2))/(energies * (np.sin(scattAngRad/2))**3) * scattAngRad_err ## mbarn
ruthCrossSection_err = np.sqrt((2*ruthCrossSection*np.cos(scattAngRad/2)/np.sin(scattAngRad/2)*scattAngRad_err)**2 +
                                (2*ruthCrossSection*0.0001/energies)**2)
ruthCrossSection_CTN_err = np.sqrt((2*ruthCrossSection_CTN*np.cos(scattAng_CTN_Rad/2)/np.sin(scattAng_CTN_Rad/2)*scattAngRad_CTN_err)**2 +
                                    (2*ruthCrossSection_CTN*0.0001/3.215)**2)

# The number of radioactive nuclei at the end  of the irradiation, from the Npeak fit, 
# for each beam energy, and each radiation type, in the format [gamma, Ka, Kb]
N_D_irr_HPGe = {
    "Ebeam=3.2MeV": {"gamma": 2.162e6, "Ka": 2.281e6, "Kb": 2.461e6},
    "Ebeam=3.5MeV": {"gamma": 8.659e6, "Ka": 9.055e6, "Kb": 9.832e6},
    "Ebeam=3.9MeV": {"gamma": 1.971e7, "Ka": 2.059e7, "Kb": 2.241e7},
    "Ebeam=4.3MeV": {"gamma": 3.853e7, "Ka": 4.009e7, "Kb": 4.382e7},
    "Ebeam=4.7MeV": {"gamma": 7.137e7, "Ka": 7.381e7, "Kb": 8.093e7},
    "Ebeam=5.0MeV": {"gamma": 1.438e8, "Ka": 1.458e8, "Kb": 1.625e8},} ## Using photopeak channel by channel yield sum

## Parameters for SDD at 8 mm
N_D_irr_SDD = {
                      "Ebeam=3.2MeV": {"Ka": 1.595e6, "Kb": 1.275e6},
                      "Ebeam=3.5MeV": {"Ka": 6.735e6, "Kb": 5.892e6},
                      "Ebeam=3.9MeV": {"Ka": 1.598e7, "Kb": 1.562e7},
                      "Ebeam=4.3MeV": {"Ka": 3.242e7, "Kb": 3.238e7},
                      "Ebeam=4.7MeV": {"Ka": 6.496e7, "Kb": 6.435e7},
                      "Ebeam=5.0MeV": {"Ka": 1.364e8, "Kb": 1.375e8},} 

## Parameters for SDD at 7 mm
""" N_D_irr_SDD = {
                      "Ebeam=3.2MeV": {"Ka": 1.282e6, "Kb": 1.057e6},
                      "Ebeam=3.5MeV": {"Ka": 5.467e6, "Kb": 4.569e6},
                      "Ebeam=3.9MeV": {"Ka": 1.291e7, "Kb": 1.194e7},
                      "Ebeam=4.3MeV": {"Ka": 2.594e7, "Kb": 2.601e7},
                      "Ebeam=4.7MeV": {"Ka": 5.205e7, "Kb": 5.335e7},
                      "Ebeam=5.0MeV": {"Ka": 1.098e8, "Kb": 1.068e8},} 
 """
N_D_irr_SDD_CTN = {"Ka": 7.105e5, "Kb": 7.308e5}

N_D_irr_SDD_CTN_err = {"Ka": 3e3, "Kb": 8e3} ## VERIFICAR ESTES VALORES !!!

## Error values of N_Dirr from the fit
N_D_irr_HPGe_err = {
    "Ebeam=3.2MeV": {"gamma": 1e3, "Ka": 2e3, "Kb": 4e3},
    "Ebeam=3.5MeV": {"gamma": 5e3, "Ka": 5e3, "Kb": 9e3},
    "Ebeam=3.9MeV": {"gamma": 1e4, "Ka": 1e4, "Kb": 2e4},
    "Ebeam=4.3MeV": {"gamma": 3e4, "Ka": 2e4, "Kb": 4e4},
    "Ebeam=4.7MeV": {"gamma": 3e4, "Ka": 2e4, "Kb": 4e4},
    "Ebeam=5.0MeV": {"gamma": 1e5, "Ka": 6e4, "Kb": 1e5},} ## Using photopeak channel by channel yield sum

N_D_irr_SDD_err = {
    "Ebeam=3.2MeV": {"Ka": 6e3, "Kb": 1e4},
    "Ebeam=3.5MeV": {"Ka": 6e3, "Kb": 2e4},
    "Ebeam=3.9MeV": {"Ka": 7e3, "Kb": 2e4},
    "Ebeam=4.3MeV": {"Ka": 3e4, "Kb": 3e4},
    "Ebeam=4.7MeV": {"Ka": 2e4, "Kb": 3e4},
    "Ebeam=5.0MeV": {"Ka": 6e4, "Kb": 3e4},} ## Using photopeak channel by channel yield sum

## Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
## t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant)

## RBS detector efficiency
epsilon_p = 4.409e-4
epsilon_p_CTN = 2.91e-4 ## VERIFICAR VALOR CORRETO !!!!

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

t_irr_CTN = 5*60 + 9 # minutes
t_irr_CTN_err = 1 # min

## Total number of backscattered protons, Np
N_p = {"Ebeam=3.2MeV": 8.40e7,
       "Ebeam=3.5MeV": 1.03e8,
       "Ebeam=3.9MeV": 5.89e7,
       "Ebeam=4.3MeV": 4.87e7,
       "Ebeam=4.7MeV": 2.64e7,
       "Ebeam=5.0MeV": 2.64e7,}

N_p_CTN = 2.77e7

## ---------------- Cross-Section Calculation ---------------- ##

## HPGe at CNA
crossSections_HPGe = {}
crossSections_HPGe_err = {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    print(f"HPGe Cross-section for {key} at CNA")

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
                (decayConstant * t_irr / (Np)))
            
            ## Compute error propagation
            sigma_err = np.sqrt((sigma/ruthCrossSection[i]/ruthCrossSection_err[i])**2 +
                                sigma**2/Np + 
                                (sigma*ruthCrossSection_err[i]/ruthCrossSection[i])**2 +
                                (sigma/N_D)**2 * N_D_err**2 + 
                                ((decayConstant*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np))**2 * t_irr_err**2 + 
                                ((t_irr*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np))**2 * decayConstant_err**2)
            
            ## Store the results
            crossSections_HPGe[key][rad_type] = sigma
            crossSections_HPGe_err[key][rad_type] = sigma_err

            print(f"{rad_type}: ({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

print(f" ------------------------- \n ------------------------- \n")

## SDD at CNA
crossSections_SDD = {}
crossSections_SDD_err = {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    print(f"SDD Cross-section for {key} at CNA")

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
                (decayConstant * t_irr / (Np)))
            
                        ## Compute error propagation
            sigma_err = np.sqrt((sigma/ruthCrossSection[i]/ruthCrossSection_err[i])**2 +
                                sigma**2/Np + 
                                (sigma/N_D)**2 * N_D_err**2 + 
                                ((decayConstant*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np))**2 * t_irr_err**2 + 
                                ((t_irr*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                                (4*np.pi * epsilon_p * N_D * ruthCrossSection[i])/(Np))**2 * decayConstant_err**2)
            
            # Store result
            crossSections_SDD[key][rad_type] = sigma
            crossSections_SDD_err[key][rad_type] = sigma_err

            print(f"{rad_type}: ({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

print(f" ------------------------- \n ------------------------- \n")

## BEGe and SDD at CTN
crossSections_BEGe = {}
crossSections_BEGe_err = {}
crossSections_SDD_CTN = {}
crossSections_SDD_CTN_err = {}

key = "Ebeam=3.215MeV"
print(f"SDD Cross-section for {key} at CTN")

crossSections_SDD_CTN[key] = {}
crossSections_SDD_CTN_err[key] = {}

Np = N_p_CTN
t_irr = t_irr_CTN
t_irr_err = t_irr_CTN_err
epsilon_p = epsilon_p_CTN

# Compute the decay factor
decayFactor = 1 - np.exp(-decayConstant * t_irr)

for rad_type, N_D in N_D_irr_SDD_CTN.items():

    ## Get N_D_irr errors
    N_D_err = N_D_irr_SDD_CTN_err[rad_type]

    ## Cross-Section calculation
    sigma = (ruthCrossSection_CTN *
        (4 * np.pi * N_D * epsilon_p) / (decayFactor) *
        (decayConstant * t_irr / (Np)))
    
    ## Compute error propagation
    sigma_err = np.sqrt((sigma/ruthCrossSection_CTN/ruthCrossSection_CTN_err)**2 +
                        sigma**2/Np + 
                        (sigma/N_D)**2 * N_D_err**2 + 
                        ((decayConstant*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                        (4*np.pi * epsilon_p * N_D * ruthCrossSection_CTN)/(Np))**2 * t_irr_err**2 + 
                        ((t_irr*np.exp(decayConstant*t_irr)*(-decayConstant*t_irr + np.exp(decayConstant * t_irr) - 1))/(np.exp(decayConstant * t_irr)-1)**2 * 
                        (4*np.pi * epsilon_p * N_D * ruthCrossSection_CTN)/(Np))**2 * decayConstant_err**2)
    
    # Store result
    crossSections_SDD_CTN[key][rad_type] = sigma
    crossSections_SDD_CTN_err[key][rad_type] = sigma_err

    print(f"{rad_type}: ({sigma:.2f} +- {sigma_err:.2f}) mb")
print()

print(f" ------------------------- \n ------------------------- \n")

## Plot the experimental data alongside different author's results
PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err)