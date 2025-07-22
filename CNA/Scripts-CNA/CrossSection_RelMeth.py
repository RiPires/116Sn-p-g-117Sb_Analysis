######################################################
## Script for calculation of reaction cross-section ##
######################################################

## ---------------------------- ##
import numpy as np
from include.PlotData import*
from include.ComputeCrossSection import*
## ---------------------------- ##

## _________________________ Constants _________________________ ##
zBeam, zTarget = 1, 50
cSpeed = 2.99792458e8 # m/s
eCharge = 1.60217663e-19 # C
epsilon0 = 8.8541878e-12 # F/m

## Scattering angles (deg -> rad)
## at CNA
scattAngDeg, scattAngDeg_err = 165, 2.3
scattAngRad = np.deg2rad(scattAngDeg)
scattAngRad_err = np.deg2rad(scattAngDeg_err)
## at CTN
scattAngDeg_CTN, scattAngDeg_CTN_err = 155, 2.
scattAng_CTN_Rad = np.deg2rad(scattAngDeg_CTN)
scattAngRad_CTN_err = np.deg2rad(scattAngDeg_CTN_err)

## 117Sb decay half-life in minutes (2.8 hours)
halfLife_min = 2.8*60
halfLife_min_err = 0.01*60 # error from literature

## Decay constant
decayConstant = np.log(2) / halfLife_min  # in min^-1
decayConstant_err = np.log(2) * halfLife_min_err / halfLife_min**2  # in min^-1

## _________________________ Rutherford Cross-Section _________________________ ##
energies = np.array([3.2, 3.5, 3.9, 4.3, 4.7, 5.0])  # MeV
dE = np.array([0.046, 0.043, 0.038, 0.035, 0.042, 0.042]) # MeV

ruth_factor = (zBeam * zTarget * eCharge / (16 * np.pi * epsilon0))**2 * 1e31
ruthCrossSection = ruth_factor / (energies * 1e6 * np.sin(scattAngRad / 2)**2)**2
#print(ruthCrossSection)
ruthCrossSection_CTN = ruth_factor / ((3.215 * 1e6 * np.sin(scattAng_CTN_Rad / 2)**2)**2)

ruthCrossSection_err = np.sqrt((2 * ruthCrossSection * np.cos(scattAngRad / 2) / np.sin(scattAngRad / 2) * scattAngRad_err)**2 +
                                (2 * ruthCrossSection * dE / energies)**2)
ruthCrossSection_CTN_err = np.sqrt((2 * ruthCrossSection_CTN * np.cos(scattAng_CTN_Rad / 2) / np.sin(scattAng_CTN_Rad / 2) * scattAngRad_CTN_err)**2 +
                                    (2 * ruthCrossSection_CTN * 0.0001 / 3.215)**2)

## _________________________ N_D_irr and Errors _________________________ ##
# Datasets: N_D_irr_HPGe, N_D_irr_HPGe_err, N_D_irr_SDD, etc.
# The number of radioactive nuclei at the end of the irradiation, from the Npeak fit, 
# for each beam energy, and each radiation type
N_D_irr_HPGe = {
    "Ebeam=3.2MeV": {"gamma": 2.793e+06, "Ka": 2.813e+06, "Kb": 2.816e+06,"511 keV": 3.060e+06, "861 keV": 1.874e+06, "1004 keV": 1.383e+06},
    "Ebeam=3.5MeV": {"gamma": 1.115e+07, "Ka": 1.110e+07, "Kb": 1.126e+07,"511 keV": 1.165e+07, "861 keV": 8.931e+06, "1004 keV": 9.326e+06},
    "Ebeam=3.9MeV": {"gamma": 2.541e+07, "Ka": 2.513e+07, "Kb": 2.562e+07,"511 keV": 3.044e+07, "861 keV": 2.040e+07, "1004 keV": 1.808e+07},
    "Ebeam=4.3MeV": {"gamma": 4.933e+07, "Ka": 4.875e+07, "Kb": 4.950e+07,"511 keV": 5.857e+07, "861 keV": 4.567e+07, "1004 keV": 4.347e+07},
    "Ebeam=4.7MeV": {"gamma": 9.364e+07, "Ka": 9.178e+07, "Kb": 9.361e+07,"511 keV": 1.231e+08, "861 keV": 8.056e+07, "1004 keV": 8.023e+07},
    "Ebeam=5.0MeV": {"gamma": 1.849e+08, "Ka": 1.765e+08, "Kb": 1.839e+08,"511 keV": 2.545e+08, "861 keV": 1.691e+08, "1004 keV": 1.628e+08}}

## Error values of N_Dirr from the fit of HPGe data
N_D_irr_HPGe_err = {
    "Ebeam=3.2MeV": {"gamma": 1e+05, "Ka": 9e+04, "Kb": 1e+05,"511 keV": 1e+05, "861 keV": 2e+05, "1004 keV": 3e+05},
    "Ebeam=3.5MeV": {"gamma": 5e+05, "Ka": 4e+05, "Kb": 4e+05,"511 keV": 2e+05, "861 keV": 3e+05, "1004 keV": 7e+05},
    "Ebeam=3.9MeV": {"gamma": 1e+06, "Ka": 8e+05, "Kb": 9e+05,"511 keV": 4e+05, "861 keV": 1e+06, "1004 keV": 1e+06},
    "Ebeam=4.3MeV": {"gamma": 2e+06, "Ka": 2e+06, "Kb": 2e+06,"511 keV": 8e+05, "861 keV": 2e+06, "1004 keV": 4e+06},
    "Ebeam=4.7MeV": {"gamma": 4e+06, "Ka": 3e+06, "Kb": 3e+06,"511 keV": 3e+06, "861 keV": 5e+05, "1004 keV": 3e+06},
    "Ebeam=5.0MeV": {"gamma": 8e+06, "Ka": 6e+06, "Kb": 7e+06,"511 keV": 9e+06, "861 keV": 9e+05, "1004 keV": 1e+07}} 

## Parameters for the detector at mean position of (12+9)/2 mm
N_D_irr_SDD = {
    "Ebeam=3.2MeV": {"Ka": 2.513e+06, "Kb": 2.139e+06, "L": 2.518e+06},
    "Ebeam=3.5MeV": {"Ka": 1.011e+07, "Kb": 9.612e+06, "L": 1.045e+07},
    "Ebeam=3.9MeV": {"Ka": 2.527e+07, "Kb": 2.547e+07, "L": 2.632e+07},
    "Ebeam=4.3MeV": {"Ka": 5.141e+07, "Kb": 5.441e+07, "L": 5.601e+07},
    "Ebeam=4.7MeV": {"Ka": 1.030e+08, "Kb": 1.076e+08, "L": 1.109e+08},
    "Ebeam=5.0MeV": {"Ka": 2.149e+08, "Kb": 2.254e+08, "L": 2.377e+08}}

## Error values of N_Dirr from the fit of SDD data 
N_D_irr_SDD_err = {
    "Ebeam=3.2MeV": {"Ka": 7e+05, "Kb": 6e+05, "L": 8e+05},
    "Ebeam=3.5MeV": {"Ka": 3e+06, "Kb": 2e+06, "L": 3e+06},
    "Ebeam=3.9MeV": {"Ka": 7e+06, "Kb": 7e+06, "L": 9e+06},
    "Ebeam=4.3MeV": {"Ka": 1e+07, "Kb": 1e+07, "L": 2e+07},  
    "Ebeam=4.7MeV": {"Ka": 3e+07, "Kb": 3e+07, "L": 4e+07},        
    "Ebeam=5.0MeV": {"Ka": 6e+07, "Kb": 6e+07, "L": 4e+07}}

## Parameters for the activation at CTN
N_D_irr_BEGe_CTN = {"gamma": 9.364e5, "Ka": 7.843e5, "Kb": 7.546e5}
N_D_irr_BEGe_CTN_err = {"gamma": 3e4, "Ka": 3e4, "Kb": 3e4}

N_D_irr_SDD_CTN = {"Ka": 1.089e6, "Kb": 1.126e6}
N_D_irr_SDD_CTN_err = {"Ka": 3e5, "Kb": 3e5}

## _________________________ Parameters _________________________ ##
epsilon_p = 4.409e-4
epsilon_p_CTN = 2.91e-4  # CHECK THIS VALUE

t_irr_min = {"Ebeam=3.2MeV": 358, "Ebeam=3.5MeV": 365, "Ebeam=3.9MeV": 360,
              "Ebeam=4.3MeV": 361, "Ebeam=4.7MeV": 347, "Ebeam=5.0MeV": 344}
t_irr_err = 1.
t_irr_CTN, t_irr_CTN_err = 5 * 60 + 9, 1

N_p = {"Ebeam=3.2MeV": 8.40e7, "Ebeam=3.5MeV": 1.03e8, "Ebeam=3.9MeV": 5.89e7,
       "Ebeam=4.3MeV": 4.87e7, "Ebeam=4.7MeV": 2.64e7, "Ebeam=5.0MeV": 2.64e7}

N_p_CTN = 2.75e7

## _________________________ Cross-Section Calculation _________________________ ##

## ---------- HPGe and SDD at CNA ------------------- ##
crossSections_HPGe, crossSections_HPGe_err = {}, {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    if key in N_D_irr_HPGe:
        crossSections_HPGe[key], crossSections_HPGe_err[key] = {}, {}
        for rad_type, N_D in N_D_irr_HPGe[key].items():
            N_D_err = N_D_irr_HPGe_err[key][rad_type]
            sigma, sigma_err = compute_cross_section(N_D, N_D_err, ruthCrossSection[i], ruthCrossSection_err[i], t_irr_min[key], N_p[key], decayConstant, epsilon_p, t_irr_err, decayConstant_err)
            crossSections_HPGe[key][rad_type] = sigma
            crossSections_HPGe_err[key][rad_type] = sigma_err
            print(f"HPGe {key} - {rad_type}:\t({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

print(" -------------------------\n -------------------------\n")

crossSections_SDD, crossSections_SDD_err = {}, {}

for i, energy in enumerate(energies):
    key = f"Ebeam={energy:.1f}MeV"
    if key in N_D_irr_SDD:
        crossSections_SDD[key], crossSections_SDD_err[key] = {}, {}
        for rad_type, N_D in N_D_irr_SDD[key].items():
            N_D_err = N_D_irr_SDD_err[key][rad_type]
            sigma, sigma_err = compute_cross_section(N_D, N_D_err, ruthCrossSection[i], ruthCrossSection_err[i], t_irr_min[key], N_p[key], decayConstant, epsilon_p, t_irr_err, decayConstant_err)
            crossSections_SDD[key][rad_type] = sigma
            crossSections_SDD_err[key][rad_type] = sigma_err
            print(f"SDD {key} - {rad_type}:\t({sigma:.2f} +- {sigma_err:.2f}) mb")
    print()

print(" -------------------------\n -------------------------\n")

## ---------- BEGe and SDD at CTN ------------------- ##
crossSections_BEGe, crossSections_BEGe_err = {}, {}
crossSections_SDD_CTN, crossSections_SDD_CTN_err = {}, {}

key = "Ebeam=3.215MeV"
crossSections_BEGe[key], crossSections_BEGe_err[key] = {}, {}
print(f"BEGe Cross-section for {key} at CTN")

for rad_type, N_D in N_D_irr_BEGe_CTN.items():
    N_D_err = N_D_irr_BEGe_CTN_err[rad_type]
    sigma, sigma_err = compute_cross_section(N_D, N_D_err, ruthCrossSection_CTN, ruthCrossSection_CTN_err, t_irr_CTN, N_p_CTN, decayConstant, epsilon_p_CTN, t_irr_err, decayConstant_err)
    crossSections_BEGe[key][rad_type] = sigma
    crossSections_BEGe_err[key][rad_type] = sigma_err
    print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")

print(" -------------------------\n -------------------------\n")

crossSections_SDD_CTN[key], crossSections_SDD_CTN_err[key] = {}, {}
print(f"SDD Cross-section for {key} at CTN")

for rad_type, N_D in N_D_irr_SDD_CTN.items():
    N_D_err = N_D_irr_SDD_CTN_err[rad_type]
    sigma, sigma_err = compute_cross_section(N_D, N_D_err, ruthCrossSection_CTN, ruthCrossSection_CTN_err, t_irr_CTN, N_p_CTN, decayConstant, epsilon_p_CTN, t_irr_err, decayConstant_err)
    crossSections_SDD_CTN[key][rad_type] = sigma
    crossSections_SDD_CTN_err[key][rad_type] = sigma_err
    print(f"{rad_type}: \t ({sigma:.2f} +- {sigma_err:.2f}) mb")

print(" -------------------------\n -------------------------\n")

## Plot the experimental data alongside different author's results
PlotMyCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE)
PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE)