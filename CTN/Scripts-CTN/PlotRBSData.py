#####################################
## Script to plot RBS spectra for  ##
#####################################

## ---------------------------- ##
import os
from include.ReadData import*
from include.PlotData import *
## ---------------------------- ##

## RBS 3-alpha calibration
""" path = '../1_Irradiation/DataFiles/Calib_3-alfa/'
for file in sorted(os.listdir(path)):
    PlotRBS(str(path+file), str(file).replace('.mpa','')) """

## RBS during activation
path = '../1_Irradiation/DataFiles/Activation/RBS/'
for file in sorted(os.listdir(path)):
    
    #Data1_x, Data1_y = ReadActivationRBS(path+file, 1) ## Detector MOV E
    Data3_x, Data3_y = ReadActivationRBS(path+file, 4) ## Detector MOV D
    PlotRBS(Data3_x, Data3_y, str(file).replace('.mpa',''))