#####################################################
## Script to plot RBS spectra for each activation ##
#####################################################

## --------------------------- ##
from include.PlotData import *
from include.ReadData import *
## --------------------------- ##

## Paths for each activation energy
Paths = ['../Activations/Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/RBS/',
         '../Activations/Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/RBS/',
         '../Activations/Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/RBS/',
         '../Activations/Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/RBS/',
         '../Activations/Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/RBS/',
         '../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/RBS/']

## Loop over each activation energy
for path in Paths:

    ## Loop over the files of each activation
    for file in sorted(os.listdir(path)):

        ## Get RBS data
        ch, y = ReadActivationRBS(str(path+file))

        ## Set label
        lab = str(file).replace('.SI2.dat', '')
        lab = path[15:27] + ' - Run: ' + lab
        
        ## Plot data
        PlotRBS(ch, y, lab)
