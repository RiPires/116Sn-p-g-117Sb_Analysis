###############################################
## Script for calculation of SDD calibration ##
#  peak centroids, and sigmas                ##
###############################################

"""
Script for fitting SDD calibration runs' peaks
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
channels = [(i+1) for i in range(2048)]

## Path to calibration files
calibFile152Eu = "../Calibrations/SDD/CalibrationRuns_PosExp/Run14_152Eu_detSDD_2mm.mca"
calibFile133Ba = "../Calibrations/SDD/CalibrationRuns_PosExp/Run15_133Ba_detSDD_2mm.mca"

## Labels for file creation and plot
lab133Ba = str('133Ba_SDD')
lab152Eu = str('152Eu_SDD')

## Calibration yield list of sources
calibYield152Eu = MCA2Lists(calibFile152Eu)[0]
calibYield133Ba = MCA2Lists(calibFile133Ba)[0]

## Energies for calibration
calibEnergies152Eu = [5.633, 6.205, 6.587, 7.178, 39.522, 40.117, 45.370, 46.578]
calibEnergies133Ba = [4.285, 4.619, 4.936, 5.28, 30.625, 30.973, 34.964, 35.822]

## Regions of interest, in channel, for each photo-peak
ROId152Eu = [175, 194, 207, 225, 1261, 1282, 1448]
ROIu152Eu = [188, 206, 218, 235, 1281, 1308, 1472]

ROId133Ba = [132, 144, 156, 168, 981, 991, 1116, 1142]
ROIu133Ba = [144, 155, 162, 173, 989, 1008, 1136, 1164]

# Initial guess
initial_guess133Ba = [
    921, 137, 2.1,  # Peak 1
    644, 148, 2.9,  # Peak 2
    182, 158, 2.4,  # Peak 3
    97, 171, 2.0,   # Peak 4
    64, 179, 2.0,   # Peak 5
    473, 987, 2.4,  # Peak 6
    776, 997, 2.4,  # Peak 7
    158, 1124, 2.4, # Peak 8
]

initial_guess152Eu = [
    1145, 181, 2.1, # Peak 1
    728, 200, 2.9,  # Peak 2
    189, 212, 2.4,  # Peak 3
    121, 231, 2.4,  # Peak 4
    142, 1271, 2.4, # Peak 5
    227, 1291, 2.4, # Peak 6
    36, 1462, 2.4   # Peak 7
]

# Fit the data
FitData(gaussian, channels, calibYield152Eu, initial_guess152Eu, lab152Eu, ROId152Eu, ROIu152Eu)
FitData(gaussian, channels, calibYield133Ba, initial_guess133Ba, lab133Ba, ROId133Ba, ROIu133Ba)

FitNGauss(nGaussian, channels, calibYield152Eu, initial_guess152Eu, lab152Eu)
FitNGauss(nGaussian, channels, calibYield133Ba, initial_guess133Ba, lab133Ba)