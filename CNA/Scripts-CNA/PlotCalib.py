#################### RiP ##########################
## Script for plotting detector calibration runs ##
###################################################

## ---------------------------- ##
import os
from include.PlotData import *
from include.ReadData import *
## ---------------------------- ##


## Plot desired run
calibHPGeFile = '../Calibrations/HPGe/CalibrationRuns_PosExp/Run05_60Co_detGe_50mm.mca'
y, ch = Ge2Lists(calibHPGeFile)
PlotLogy(ch, y, calibHPGeFile.replace('../Calibrations/HPGe/CalibrationRuns_PosExp/',''))

""" ## HPGe detector path
calibPathHPGe = '../Calibrations/HPGe/CalibrationRuns_PosExp/'
## Loop over HPGe calibration runs
for file in os.listdir(calibPathHPGe):
    y, ch = Ge2Lists(str(calibPathHPGe+file))
    PlotLogy(ch, y, str(file).replace('.mca', '')) """

""" ## SDD detector path
calibPathSDD = '../Calibrations/SDD/CalibrationRuns_PosExp/'
## Loop over SDD calibration runs
for file in os.listdir(calibPathSDD):
    y, ch = MCA2Lists(str(calibPathSDD+file))
    Plot(ch, y, str(file).replace('.mca', '')) """