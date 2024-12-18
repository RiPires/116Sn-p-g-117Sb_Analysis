##############################################
## Script for calculation of SDD resolution ##
##############################################

"""
Resolution is defined as: 

R(E) = FWHM/E

With a known source, we can calibrate the energy resolution as the following linear funtion:

R(E) = b/sqrt(E) + c

If necessary, a quadratic regression may be applied:

R(E) = a/E + b/sqrt(E) + c
"""

## ---------------------------- ##
from include.ReadData import*
from include.Calibration import*
from include.Analyse import*
import numpy as np
## ---------------------------- ##

## Path to calibration files
calibFile152Eu = "../Calibrations/SDD/CalibrationRuns_PosExp/Run11_152Eu_detSDD_16mm.mca"
calibFile137Cs = "../Calibrations/SDD/CalibrationRuns_PosExp/Run12_137Cs_detSDD_16mm.mca"
calibFile133Ba = "../Calibrations/SDD/CalibrationRuns_PosExp/Run13_133Ba_detSDD_16mm.mca"

## Calibration yield list of sources
calibYield152Eu = MCA2Lists(calibFile152Eu)[0]
calibYield137Cs = MCA2Lists(calibFile137Cs)[0]
calibYield133Ba = MCA2Lists(calibFile133Ba)[0]

## Energies for calibration
calibEnergies152Eu = [5.633, 6.205, 6.587, 7.178, 39.522, 40.117, 45.370, 46.578]
calibEnergies133Ba = [4.285, 4.619, 4.936, 5.28, 30.625, 30.973, 34.964, 35.822]
calibEnergies137Cs = [661.66]

## Regions of interest, in channel, for each photo-peak
ROId152Eu = [175, 194, 207, 225, 1261, 1282, 1448, 1491]
ROIu152Eu = [188, 206, 218, 235, 1281, 1308, 1472, 1505]

ROId133Ba = [132, 144, 156, 168, 981, 991, 1116, 1142]
ROIu133Ba = [144, 155, 162, 173, 989, 1008, 1136, 1164]

ROId137Cs = [2037]
ROIu137Cs = [2071]

## Analyse calibration run
calibCents, calibErrs, calibSigmas, calibFWHM = Analyze(calibYield152Eu, ROId152Eu, ROIu152Eu)

## Write analysis to output file
with open("AnalyseCalibSpectra_152Eu.txt", "w") as file:
    header = "Peak nr. \t Energy (keV) \t ROId \t ROIu \t Centroid \t Sigma \t FWHM \n"
    file.write(header)
    for i in range(len(calibEnergies152Eu)):
        file.write(str(i+1)+'\t'+
                   str(calibEnergies152Eu[i])+'\t'+
                   str(ROId152Eu[i])+'\t'+
                   str(ROIu152Eu[i])+'\t'+
                   str(calibCents[i])+'\t'+
                   str(calibSigmas[i])+'\t'+
                   str(calibFWHM[i])+'\n')    

    file.close()

## Perform calibration
m, b, dm, db = Calib(calibEnergies152Eu, calibCents, calibErrs)

## Calculate Resolution: R = FWHM/E
Res = [(calibFWHM[i]/calibEnergies152Eu[i] * 100) for i in range(len(calibEnergies152Eu))] ## in percentage

oneOverSqrtE = [(1/np.sqrt(calibEnergies152Eu[i])) for i in range(len(calibEnergies152Eu))]

## Perform the linear regression for resolution

## start with a fake error in 1/sqrt(E), will then calculate the real value
res_err = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]

res_m, res_b, res_dm, res_db = Resolution(Res, oneOverSqrtE, res_err)

