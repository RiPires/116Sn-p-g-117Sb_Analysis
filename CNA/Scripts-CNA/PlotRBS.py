#####################################################
## Script to plot RBS spectra for each activation ##
#####################################################

## -------------------- ##
from PlotData import *
from ReadData import *
## -------------------- ##

## Paths for each activation energy
Paths = ['../Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/RBS/',
        '../Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/RBS/',
        '../Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/RBS/',
        '../Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/RBS/',
        '../Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/RBS/',
        '../Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/RBS/']

## Loop over each activation
for path in Paths:
    ## Loop over the files of each activation
    for file in os.listdir(path):
        ch, y = ReadActivationRBS(str(path+file))
        lab = str(file).replace('.SI2.dat', '')
        PlotRBS(ch, y, lab)
