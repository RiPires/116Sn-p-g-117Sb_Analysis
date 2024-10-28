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
from ReadData import*
from Calibration import*
from Analyse import*
import numpy as np
## ---------------------------- ##

## Path to calibration file
calibFile = "../Calibrations/HPGe/CalibrationRuns_PosExp/Run10_152Eu_detGe_8mm.mca"

## Calibration yield list of 152Eu source
calibYield = Ge2Lists(calibFile)[0]

## 152Eu energies for calibration
calibEnergies = [121.78, 244.70, 344.28, 411.12, 443.96, 778.9, 867.38, 964.06, 1085.84, 1112.08]

## Regions of interest, in channel, for each photo-peak of 152Eu
ROId = [366, 747, 1057, 1267, 1369, 2399, 2679, 2978, 3358, 3432]
ROIu = [393, 771, 1081, 1282, 1385, 2431, 2699, 3001, 3373, 3458]

## Analyse calibration run
calibCents, calibErrs, calibSigmas, calibFWHM = Analyze(calibYield, ROId, ROIu)
print('Centroids: ', calibCents, '\n')
print('FWHM: ', calibFWHM, '\n') 

## Perform calibration
m, b, dm, db = Calib(calibEnergies, calibCents, calibErrs)

## Calculate Resolution: R = FWHM/E
Res = [(calibFWHM[i]/calibEnergies[i] * 100) for i in range(len(calibEnergies))] ## in percentage

oneOverSqrtE = [(1/np.sqrt(calibEnergies[i])) for i in range(len(calibEnergies))]

## Perform the linear regression for resolution

## start with a fake error in 1/sqrt(E), will then calculate the real value
res_err = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]

res_m, res_b, res_dm, res_db = Resolution(Res, oneOverSqrtE, res_err)

