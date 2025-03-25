############## RiP #################
## Script for removing background ##
####################################

## ---------------------------- ##
import os
from include.PlotData import *
from include.ReadData import *
from include.Merge import *
## ---------------------------- ##

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
def RemoveBg(dataFile):
    """
    Function that removes the background rate of an input dataFile, using the
    Backgroud measurement data. Writes out a new file with background removed.

    INPUTS: 
        - dataFile (str): path for data file; 
    """
    print('Removing background from file: ', dataFile)

    ## Check detector HPGe or SDD from file name
    if "HPGe" in dataFile:

        ## Set HPGe channels     
        ch = [(i+1) for i in range(4096)]

        ## Get run yield and acquisition live time   
        runYield, _, acquiTime = Ge2Lists(dataFile)

        ## Background runs path
        bgPath = '../Calibrations/HPGe/Background/'

        ## Get background merged yield and time
        mergeBgYield, bgTime = Merge(bgPath, 'ge')

    elif "SDD" in dataFile:

        ## Set SDD channels
        ch = [(i+1) for i in range(2048)]

        ## Get run yield and acquisiton live time
        runYield, _, acquiTime = MCA2Lists(dataFile)

        ## Background runs path
        bgPath = '../Calibrations/SDD/Background/'

        ## Get background merged yield and time
        mergeBgYield, bgTime = Merge(bgPath, 'sdd')

    #print(f"Time = {bgTime:.0f}")
        
    ## Converts run yield into count rate (in s^-1)
    runRate = [runYield[i]/acquiTime for i in range(len(runYield))]

    ## Converts background yield into background count rate (in s^-1)
    bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]

    ## Remove background rate from run data 
    runRateBgRem = [(runRate[i] - bgRate[i]) for i in range(len(runRate))]

    ## Set labels
    lab = dataFile[-63:-51] + ': ' + dataFile[-26:-4]
    bgLab = 'Background Rate'
    rateLab = lab +'_BG removed'

    ## Plot both run data, bg rate and run data with bg removed 
    #Plot3RateLogy(ch, runRate, bgRate, runRateBgRem, lab, bgLab, rateLab)

    ## Save run rate with background removed values to file 
    with open(dataFile.replace(".mca","_BgRemoved.mca"), 'w') as outFile:
        counts = 0
        for rate in runRateBgRem:
            if rate <= 0:
                outFile.write(f"{counts:.0f}\n")
            elif rate > 0:
                counts = int(rate * acquiTime)      ## convert count rate back to counts
                outFile.write(f"{counts:.0f}\n")
    outFile.close()

    return
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #

##  ***********************************************************  ##
##               Perform background removal here                 ##
##  ***********************************************************  ##

## Choose paths for data files
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/',]

gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/',]

 
## For each path, remove background for every data file
for path in gePaths:
    for file in sorted(os.listdir(path)):
        RemoveBg(str(path+file))

## For specific data file
#filePath = '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/116Sn-D5_Decay_SDD_084.mca'
#RemoveBg(filePath)