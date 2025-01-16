#################### RiP ###########
## Script for removing background ##
####################################

## ---------------------------- ##
import os
from include.PlotData import *
from include.ReadData import *
from include.Merge import *
## ---------------------------- ##

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
        calibYield, _, acquiTime = Ge2Lists(dataFile)
        ## Background runs path
        bgPath = '../Calibrations/HPGe/Background/'
        ## Merge background yield
        mergeBgYield = Merge(bgPath, 'ge')
        ## Background acquisition time
        bgTime = 35*1800 + 777 ## seconds: 35 full runs * 1800 sec each + 777 sec last run

    elif "SDD" in dataFile:
        calibYield, _, acquiTime = MCA2Lists(dataFile)
        ## Background runs path
        bgPath = '../Calibrations/SDD/Background/'
        ## Merge background yield
        mergeBgYield = Merge(bgPath, 'sdd')
        ## Background acquisition time
        bgTime = 45954 ## seconds
        
    ## Converts data counts to count rate (in s^-1)
    calibRate = [calibYield[i]/acquiTime for i in range(len(calibYield))]
    ## Converts background counts to background count rate (in s^-1)
    bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]
    ## Remove background rate from file 
    calibRateBgRem = [(calibRate[i] - bgRate[i]) for i in range(len(calibRate))]

    ## Set Energy axes
    ch_hpge = [(i+1) for i in range(4096)]
    ch_sdd = [(i+1) for i in range(2048)]

    ## Set label
    lab = dataFile[-63:-51] + ': ' + dataFile[-26:-4]
    ## Set label
    bgLab = 'Background Rate'
    ## Set label
    rateLab = lab +'_BG removed'
    ## Background rate

    ## Plot both calib, bg rate and calib with bg removed 
    Plot3RateLogy(ch_hpge, calibRate, bgRate, calibRateBgRem, lab, bgLab, rateLab)

    ## Save calibration rate with background removed values to file 
    """     with open(dataFile.replace(".mca","_BgRemoved.mca"), 'w') as outFile:
        counts = 0
        for rate in calibRateBgRem:
            if rate <= 0:
                outFile.write(f"{counts:.0f}\n")
            elif rate > 0:
                counts = int(rate * acquiTime)      ## convert count rate back to counts
                outFile.write(f"{counts:.0f}\n")
    outFile.close() """

    return

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

## For specific data file
filePath = '../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/116Sn-C3_Decay_HPGe-089.mca'
RemoveBg(filePath)

## For each path, remove background for every data file
for path in gePaths:
    for file in os.listdir(path):
        RemoveBg(str(path+file))