################################################
## Script for calculation of HPGe calibration ##
#  peak centroids, and sigmas                 ##
################################################

"""
Script for fitting HPGe calibration runs' peaks
 returning mean value and standard deviation for further energy
 and resolution calibration
"""

## ---------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *

from include.ReadData import*
from include.Calibration import*
from include.Analyse import*
from include.Fits import*
## ---------------------------- ##

## Channels list
channels = [(i+1) for i in range(4096)]

## Path to calibration files
calibFile152Eu = "../Calibrations/HPGe/CalibrationRuns_PosExp/BgRemoved/Run03_152Eu_50mm_BgRemoved.mca"
calibFile137Cs = "../Calibrations/HPGe/CalibrationRuns_PosExp/BgRemoved/Run02_137Cs_50mm_BgRemoved.mca"
calibFile133Ba = "../Calibrations/HPGe/CalibrationRuns_PosExp/BgRemoved/Run04_133Ba_50mm_BgRemoved.mca"
calibFile60Co = "../Calibrations/HPGe/CalibrationRuns_PosExp/BgRemoved/Run05_60Co_50mm_BgRemoved.mca"

## Labels for file creation and plot
lab60Co = str('60Co')
lab133Ba = str('133Ba')
lab137Cs = str('137Cs')
lab152Eu = str('152Eu')

## Calibration yield list of sources
calibYield152Eu = Ge2ListsBgRm(calibFile152Eu)[0]
calibYield137Cs = Ge2ListsBgRm(calibFile137Cs)[0]
calibYield133Ba = Ge2ListsBgRm(calibFile133Ba)[0]
calibYield60Co = Ge2ListsBgRm(calibFile60Co)[0]

## Energies for calibration
calibEnergies152Eu = [121.78, 244.70, 344.28, 411.12, 443.96, 778.9, 867.38, 964.06, 1085.84, 1112.08]
calibEnergies137Cs = [661.66]
calibEnergies133Ba = [81., 276.4, 302.85, 356.01, 383.85]
calibEnergies60Co = [1173.2]

## Regions of interest, in channel, for each photo-peak
ROId152Eu = [366, 747, 1057, 1267, 1369, 2399, 2679, 2978, 3358, 3432]
ROIu152Eu = [393, 771, 1081, 1282, 1385, 2431, 2699, 3001, 3373, 3458]

ROId137Cs = [88, 107, 2037]
ROIu137Cs = [106, 120, 2071]

ROId133Ba = [240, 850, 931, 1095, 1184]
ROIu133Ba = [261, 865, 947, 1117, 1195]

ROId60Co = [3617]
ROIu60Co = [3651]

# Initial guesses
initial_guess152Eu = [
    8873, 379, 1.0,
    1268, 760, 1.0, 
    3040, 1068, 1.0, 
    213, 1276, 1.0, 
    270, 1377, 1.0, 
    515, 2416, 1.0, 
    150, 2690, 1.0, 
    424, 2990, 1.0, 
    266, 3376, 1.0, 
    335, 3449, 1.0
]

initial_guess137Cs = [
    2106, 100, 1.0,
    479, 114, 1.0,
    4635, 2050, 1.0]

initial_guess133Ba = [
    11630, 250, 2.0,
    1041, 857, 2.0,
    2329, 939, 2.0,
    6238, 1105, 2.0,
    920, 1190, 2.0
]

initial_guess60Co = [1863, 3638, 2.0]

# Fit the data
FitData(gaussian, channels, calibYield152Eu, initial_guess152Eu, lab152Eu, ROId152Eu, ROIu152Eu)
FitData(gaussian, channels, calibYield137Cs, initial_guess137Cs, lab137Cs, ROId137Cs, ROIu137Cs)
FitData(gaussian, channels, calibYield133Ba, initial_guess133Ba, lab133Ba, ROId133Ba, ROIu133Ba)
FitData(gaussian, channels, calibYield60Co, initial_guess60Co, lab60Co, ROId60Co, ROIu60Co)