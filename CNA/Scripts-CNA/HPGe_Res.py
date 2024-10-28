###############################################
## Script for calculation of HPGe resolution ##
###############################################

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
calibFile152Eu = "../Calibrations/HPGe/CalibrationRuns_PosExp/Run10_152Eu_detGe_8mm.mca"
calibFile133Ba = "../Calibrations/HPGe/CalibrationRuns_PosExp/Run09_133Ba_detGe_8mm.mca"
calibFile137Cs = "../Calibrations/HPGe/CalibrationRuns_PosExp/Run01_137Cs_detGe_8mm.mca"
calibFile60Co = "../Calibrations/HPGe/CalibrationRuns_PosExp/Run05_60Co_detGe_50mm.mca"

## Calibration yield list of sources
calibYield152Eu = Ge2Lists(calibFile152Eu)[0]
calibYield133Ba = Ge2Lists(calibFile133Ba)[0]
calibYield137Cs = Ge2Lists(calibFile137Cs)[0]
calibYield60Co = Ge2Lists(calibFile60Co)[0]

## Energies for calibration
calibEnergies152Eu = [121.78, 244.70, 344.28, 411.12, 443.96, 778.9, 867.38, 964.06, 1085.84, 1112.08]
calibEnergies133Ba = [81., 276.4, 302.85, 356.01, 383.85]
calibEnergies137Cs = [661.66]
calibEnergies60Co = [1173.2]

## Regions of interest, in channel, for each photo-peak
ROId152Eu = [366, 747, 1057, 1267, 1369, 2399, 2679, 2978, 3358, 3432]
ROIu152Eu = [393, 771, 1081, 1282, 1385, 2431, 2699, 3001, 3373, 3458]

ROId133Ba = [240, 850, 931, 1095, 1184]
ROIu133Ba = [261, 865, 947, 1117, 1195]

ROId137Cs = [2037]
ROIu137Cs = [2071]

ROId60Co = [3617]
ROIu60Co = [3651]

## Analyse calibration run
calibCents, calibErrs, calibSigmas, calibFWHM = Analyze(calibYield60Co, ROId60Co, ROIu60Co)

## Write analysis to output file
with open("AnalyseCalibSpectra.txt", "w") as file:
    header = "Peak nr. \t Energy (keV) \t ROId \t ROIu \t Centroid \t Sigma \t FWHM \n"
    file.write(header)
    for i in range(len(calibEnergies60Co)):
        file.write(str(i+1)+'\t'+
                   str(calibEnergies60Co[i])+'\t'+
                   str(ROId60Co[i])+'\t'+
                   str(ROIu60Co[i])+'\t'+
                   str(calibCents[i])+'\t'+
                   str(calibSigmas[i])+'\t'+
                   str(calibFWHM[i])+'\n')    

    file.close()

## Perform calibration
m, b, dm, db = Calib(calibEnergies, calibCents, calibErrs)

## Calculate Resolution: R = FWHM/E
Res = [(calibFWHM[i]/calibEnergies[i] * 100) for i in range(len(calibEnergies))] ## in percentage

oneOverSqrtE = [(1/np.sqrt(calibEnergies[i])) for i in range(len(calibEnergies))]

## Perform the linear regression for resolution

## start with a fake error in 1/sqrt(E), will then calculate the real value
res_err = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]

res_m, res_b, res_dm, res_db = Resolution(Res, oneOverSqrtE, res_err)

