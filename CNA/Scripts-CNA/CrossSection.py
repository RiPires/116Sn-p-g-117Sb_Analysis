######################################################
## Script for calculation of reaction cross-section ##
######################################################

## ---------------------------- ##
import numpy as np
from include.PlotData import*
## ---------------------------- ##

## _________________________ Constants _________________________ ##
zBeam = 1
zTarget = 50
cSpeed = 2.99792458e8 # m/s
eCharge = 1.60217663e-19 # C
epsilon0 = 8.8541878e-12 # F/m

## Scattering angle at CNA
scattAngDeg = 165 # deg
scattAngDeg_err = 2.3 # deg
scattAngRad = np.deg2rad(scattAngDeg) # radians
scattAngRad_err = np.deg2rad(scattAngDeg_err) # radians

## Scattering angle at CTN
scattAngDeg_CTN = 155 # deg
scattAngDeg_CTN_err = 2. # deg # VERIFICAR ESTE VALOR !!!
scattAng_CTN_Rad = np.deg2rad(scattAngDeg_CTN) # radians
scattAngRad_CTN_err = np.deg2rad(scattAngDeg_CTN_err) # radians

## 117Sb decay half-life in minutes (2.8 hours)
halfLife_min = 2.8*60 # minutes
halfLife_min_err = 0.01*60 # minutes - error from literature

## Decay constant
decayConstant = np.log(2) / halfLife_min  # in min^-1
decayConstant_err = np.log(2) * halfLife_min_err / halfLife_min**2  # in min^-1
## _____________________________________________________________ ## 

## Calculate Rutherford Differential Cross-Section
energies = np.array([3.2, 3.5, 3.9, 4.3, 4.7, 5.0]) # MeV
dE = np.array([0.046, 0.043, 0.038, 0.035, 0.042, 0.042])
ruthCrossSection = ( (zBeam*zTarget*eCharge) / (16*np.pi*epsilon0*energies*10**6*np.sin(scattAngRad/2)**2) )**2 *1e31 # mb/sr
ruthCrossSection_CTN = ( (zBeam*zTarget*eCharge) / (16*np.pi*epsilon0*3.215*10**6*np.sin(scattAng_CTN_Rad/2)**2) )**2 *1e31 # mb/sr

## Compute error propagation
#alfa = ((zBeam*zTarget*eCharge)/(16*np.pi*epsilon0*10**6))**2 * 10**31
#ruthCrossSection_err = (alfa * np.cos(scattAngRad/2))/(energies * (np.sin(scattAngRad/2))**3) * scattAngRad_err ## mbarn
ruthCrossSection_err = np.sqrt((2*ruthCrossSection*np.cos(scattAngRad/2)/np.sin(scattAngRad/2)*scattAngRad_err)**2 +
                                (2*ruthCrossSection*dE/energies)**2)
ruthCrossSection_CTN_err = np.sqrt((2*ruthCrossSection_CTN*np.cos(scattAng_CTN_Rad/2)/np.sin(scattAng_CTN_Rad/2)*scattAngRad_CTN_err)**2 +
                                    (2*ruthCrossSection_CTN*0.0001/3.215)**2)

# The number of radioactive nuclei at the end  of the irradiation, from the Npeak fit, 
# for each beam energy, and each radiation type
N_D_irr_HPGe = {
    "Ebeam=3.2MeV": {"gamma": 2.879e6, "Ka": 2.754e6, "Kb": 2.908e6, "511 keV": 3.162e6, "861 keV": 1.990e6, "1004 keV": 1.471e6},
    "Ebeam=3.5MeV": {"gamma": 1.153e7, "Ka": 1.094e7, "Kb": 1.167e7, "511 keV": 1.209e7, "861 keV": 9.367e6, "1004 keV": 9.896e6},
    "Ebeam=3.9MeV": {"gamma": 2.630e7, "Ka": 2.490e7, "Kb": 2.662e7, "511 keV": 3.168e7, "861 keV": 2.126e7, "1004 keV": 1.877e7},
    "Ebeam=4.3MeV": {"gamma": 5.135e7, "Ka": 4.849e7, "Kb": 5.174e7, "511 keV": 6.151e7, "861 keV": 4.807e7, "1004 keV": 4.559e7},
    "Ebeam=4.7MeV": {"gamma": 9.499e7, "Ka": 8.922e7, "Kb": 9.537e7, "511 keV": 1.256e8, "861 keV": 8.266e7, "1004 keV": 8.243e7},
    "Ebeam=5.0MeV": {"gamma": 1.923e8, "Ka": 1.764e8, "Kb": 1.923e8, "511 keV": 2.668e8, "861 keV": 1.787e8, "1004 keV": 1.712e8}}

## Error values of N_Dirr from the fit of HPGe data
N_D_irr_HPGe_err = {
    "Ebeam=3.2MeV": {"gamma": 9e4, "Ka": 5e4, "Kb": 8e4, "511 keV": 5e4, "861 keV": 2e5, "1004 keV": 2e5},
    "Ebeam=3.5MeV": {"gamma": 3e5, "Ka": 2e5, "Kb": 3e5, "511 keV": 2e5, "861 keV": 2e5, "1004 keV": 5e5},
    "Ebeam=3.9MeV": {"gamma": 8e5, "Ka": 4e5, "Kb": 7e5, "511 keV": 3e5, "861 keV": 9e5, "1004 keV": 6e5},
    "Ebeam=4.3MeV": {"gamma": 2e6, "Ka": 8e5, "Kb": 1e6, "511 keV": 6e5, "861 keV": 2e6, "1004 keV": 2e6},
    "Ebeam=4.7MeV": {"gamma": 3e6, "Ka": 2e6, "Kb": 2e6, "511 keV": 2e6, "861 keV": 4e5, "1004 keV": 2e6},
    "Ebeam=5.0MeV": {"gamma": 6e6, "Ka": 3e6, "Kb": 5e6, "511 keV": 7e6, "861 keV": 8e5, "1004 keV": 9e6}} 

## Parameters for the detector at mean position of (12+10)/2 mm
N_D_irr_SDD = {
                      "Ebeam=3.2MeV": {"Ka": 2.430e6, "Kb": 1.925e6},
                      "Ebeam=3.5MeV": {"Ka": 1.023e7, "Kb": 9.097e6},
                      "Ebeam=3.9MeV": {"Ka": 2.435e7, "Kb": 2.316e7},
                      "Ebeam=4.3MeV": {"Ka": 4.932e7, "Kb": 4.947e7},
                      "Ebeam=4.7MeV": {"Ka": 9.891e7, "Kb": 9.906e7},
                      "Ebeam=5.0MeV": {"Ka": 2.035e8, "Kb": 2.031e8}}

## Error values of N_Dirr from the fit of SDD data 
N_D_irr_SDD_err = {
    "Ebeam=3.2MeV": {"Ka": 7e5, "Kb": 5e5},
    "Ebeam=3.5MeV": {"Ka": 3e6, "Kb": 2e6},
    "Ebeam=3.9MeV": {"Ka": 7e6, "Kb": 6e6},
    "Ebeam=4.3MeV": {"Ka": 1e7, "Kb": 1e7},
    "Ebeam=4.7MeV": {"Ka": 3e7, "Kb": 2e7},
    "Ebeam=5.0MeV": {"Ka": 5e7, "Kb": 5e7}}

## Parameters for the activation at CTN
N_D_irr_BEGe_CTN = {"gamma": 8.429e5, "Ka": 8.728e5, "Kb": 8.419e5}
N_D_irr_BEGe_CTN_err = {"gamma": 3e4, "Ka": 3e4, "Kb": 3e4}

N_D_irr_SDD_CTN = {"Ka": 1.089e6, "Kb": 1.126e6}
N_D_irr_SDD_CTN_err = {"Ka": 3e5, "Kb": 3e5}

## Compute the reaction cross-section using the known values for epsilon_P (RBS detector resolution),
## t_irr (irradiation time), w_A (isotopic enrichement of the target), t_irr (irradiation time), and lambda (decay constant)

## RBS detector efficiency
epsilon_p = 4.409e-4
epsilon_p_CTN = 2.91e-4 ## VERIFICAR VALOR CORRETO !!!!

## Total irradiation time, in minutes, for each activation
t_irr_min = {"Ebeam=3.2MeV": 358,
             "Ebeam=3.5MeV": 365,  
             "Ebeam=3.9MeV": 360,
             "Ebeam=4.3MeV": 361,
             "Ebeam=4.7MeV": 347,
             "Ebeam=5.0MeV": 344}
t_irr_err = 1. # minute

t_irr_CTN = 5*60 + 9 # minutes
t_irr_CTN_err = 1 # min

## Total number of backscattered protons, Np
N_p = {"Ebeam=3.2MeV": 8.40e7,
       "Ebeam=3.5MeV": 1.03e8,
       "Ebeam=3.9MeV": 5.89e7,
       "Ebeam=4.3MeV": 4.87e7,
       "Ebeam=4.7MeV": 2.64e7,
       "Ebeam=5.0MeV": 2.64e7}

N_p_CTN = 2.75e7

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

            print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")
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

            print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

print(f" ------------------------- \n ------------------------- \n")

## BEGe and SDD at CTN
crossSections_BEGe = {}
crossSections_BEGe_err = {}
crossSections_SDD_CTN = {}
crossSections_SDD_CTN_err = {}

key = "Ebeam=3.215MeV"

Np = N_p_CTN
t_irr = t_irr_CTN
t_irr_err = t_irr_CTN_err
epsilon_p = epsilon_p_CTN

# Compute the decay factor
decayFactor = 1 - np.exp(-decayConstant * t_irr)

## BEGe
print(f"BEGe Cross-section for {key} at CTN")

crossSections_BEGe[key] = {}
crossSections_BEGe_err[key] = {}

for rad_type, N_D in N_D_irr_BEGe_CTN.items():

    ## Get N_D_irr errors
    N_D_err = N_D_irr_BEGe_CTN_err[rad_type]

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
    crossSections_BEGe[key][rad_type] = sigma
    crossSections_BEGe_err[key][rad_type] = sigma_err

    print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")
print()

print(f" ------------------------- \n ------------------------- \n")

## SDD
print(f"SDD Cross-section for {key} at CTN")

crossSections_SDD_CTN[key] = {}
crossSections_SDD_CTN_err[key] = {}

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

    print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")
print()

print(f" ------------------------- \n ------------------------- \n")

## Plot the experimental data alongside different author's results
PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE)