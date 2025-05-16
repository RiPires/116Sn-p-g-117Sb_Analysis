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
dE = np.array([0.046, 0.043, 0.038, 0.035, 0.042, 0.042])

ruth_factor = (zBeam * zTarget * eCharge / (16 * np.pi * epsilon0))**2 * 1e31
ruthCrossSection = ruth_factor / (energies * 1e6 * np.sin(scattAngRad / 2)**2)**2
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
    "Ebeam=3.2MeV": {"gamma": 2.886e6, "Ka": 2.907e6, "Kb": 2.908e6, "511 keV": 3.162e6, "861 keV": 1.990e6, "1004 keV": 1.471e6},
    "Ebeam=3.5MeV": {"gamma": 1.156e7, "Ka": 1.151e7, "Kb": 1.167e7, "511 keV": 1.209e7, "861 keV": 9.367e6, "1004 keV": 9.896e6},
    "Ebeam=3.9MeV": {"gamma": 2.640e7, "Ka": 2.612e7, "Kb": 2.662e7, "511 keV": 3.168e7, "861 keV": 2.126e7, "1004 keV": 1.877e7},
    "Ebeam=4.3MeV": {"gamma": 5.156e7, "Ka": 5.095e7, "Kb": 5.174e7, "511 keV": 6.151e7, "861 keV": 4.807e7, "1004 keV": 4.559e7},
    "Ebeam=4.7MeV": {"gamma": 9.539e7, "Ka": 9.351e7, "Kb": 9.537e7, "511 keV": 1.256e8, "861 keV": 8.266e7, "1004 keV": 8.243e7},
    "Ebeam=5.0MeV": {"gamma": 1.934e8, "Ka": 1.847e8, "Kb": 1.923e8, "511 keV": 2.668e8, "861 keV": 1.787e8, "1004 keV": 1.712e8}}

## Error values of N_Dirr from the fit of HPGe data
N_D_irr_HPGe_err = {
    "Ebeam=3.2MeV": {"gamma": 1e5, "Ka": 9e4, "Kb": 1e5, "511 keV": 5e4, "861 keV": 2e5, "1004 keV": 2e5},
    "Ebeam=3.5MeV": {"gamma": 5e5, "Ka": 4e5, "Kb": 4e5, "511 keV": 2e5, "861 keV": 2e5, "1004 keV": 5e5},
    "Ebeam=3.9MeV": {"gamma": 1e6, "Ka": 8e5, "Kb": 1e6, "511 keV": 3e5, "861 keV": 9e5, "1004 keV": 6e5},
    "Ebeam=4.3MeV": {"gamma": 2e6, "Ka": 2e6, "Kb": 2e6, "511 keV": 6e5, "861 keV": 2e6, "1004 keV": 2e6},
    "Ebeam=4.7MeV": {"gamma": 4e6, "Ka": 3e6, "Kb": 3e6, "511 keV": 2e6, "861 keV": 4e5, "1004 keV": 2e6},
    "Ebeam=5.0MeV": {"gamma": 8e6, "Ka": 6e6, "Kb": 7e6, "511 keV": 7e6, "861 keV": 8e5, "1004 keV": 9e6}} 

## Parameters for the detector at mean position of (12+9)/2 mm
N_D_irr_SDD = {
    "Ebeam=3.2MeV": {"Ka": 2.494e+06, "Kb": 2.098e+06},
    "Ebeam=3.5MeV": {"Ka": 1.012e+07, "Kb": 9.456e+06},
    "Ebeam=3.9MeV": {"Ka": 2.546e+07, "Kb": 2.518e+07},
    "Ebeam=4.3MeV": {"Ka": 5.126e+07, "Kb": 5.509e+07},
    "Ebeam=4.7MeV": {"Ka": 1.026e+08, "Kb": 1.072e+08},
    "Ebeam=5.0MeV": {"Ka": 2.166e+08, "Kb": 2.264e+08}}

## Error values of N_Dirr from the fit of SDD data 
N_D_irr_SDD_err = {
    "Ebeam=3.2MeV": {"Ka": 2e5, "Kb": 3e5},
    "Ebeam=3.5MeV": {"Ka": 8e5, "Kb": 1e6},
    "Ebeam=3.9MeV": {"Ka": 2e6, "Kb": 2e6},
    "Ebeam=4.3MeV": {"Ka": 4e6, "Kb": 7e6},
    "Ebeam=4.7MeV": {"Ka": 8e6, "Kb": 7e6},
    "Ebeam=5.0MeV": {"Ka": 2e7, "Kb": 2e7}}

## Parameters for the activation at CTN
N_D_irr_BEGe_CTN = {"gamma": 8.429e5, "Ka": 8.728e5, "Kb": 8.419e5}
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
PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE)