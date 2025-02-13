#####################################################
## Script to plot RBS spectra for each activation ##
#####################################################

## -------------------- ##
from include.PlotData import *
from include.ReadData import *
## -------------------- ##

## Paths for each activation energy
Paths = ['../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/RBS/']

## Loop over each activation
for path in Paths:
    ## Loop over the files of each activation
    for file in os.listdir(path):
        ch, y = ReadActivationRBS(str(path+file))
        lab = str(file).replace('.SI2.dat', '')
        PlotRBS(ch, y, lab)
