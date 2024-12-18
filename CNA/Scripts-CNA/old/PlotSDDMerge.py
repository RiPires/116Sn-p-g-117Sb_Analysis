########################  RiP  #############################
## Script for plotting SDD merged yield of different runs ##
############################################################

## ---------------------------- ##
from PlotData import *
from Merge import *
## ---------------------------- ##

## Set channel axes
ch_sdd = [(i+1) for i in range(2048)]

## SDD decay data files paths
sddPaths = ['../Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
            '../Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
            '../Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
            '../Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
            '../Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
            '../Ebeam=5.0MeV/2_Decay/DataFiles_SDD/']

## Loop over different activation energies
for path in sddPaths:

    ## Merge decay runs
    mergeYieldSDD = Merge(path, 'sdd')

    ## Plot merged yield sdd
    lab = path[3:15]
    Plot(ch_sdd, mergeYieldSDD, str(lab))