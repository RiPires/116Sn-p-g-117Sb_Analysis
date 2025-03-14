#####################################
## Script to plot RBS spectra for  ##
#####################################

## ---------------------------- ##
import os
from include.ReadData import*
from include.PlotData import *
## ---------------------------- ##

## RBS 3-alpha calibration
path = '../1_Irradiation/DataFiles/Calib_3-alfa/'
for file in os.listdir(path):
    PlotRBS(str(path+file), str(file).replace('.mpa',''))

## RBS during activation
path = '../1_Irradiation/DataFiles/Activation/RBS/'
for file in os.listdir(path):
    PlotRBS(str(path+file), str(file).replace('.mpa',''))