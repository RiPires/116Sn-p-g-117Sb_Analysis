#################### RiP ###########################
## Script for removing background from the 152Eu  ##
## calibration run                                ##
####################################################

## ---------------------------- ##
import os

from include.PlotData import *
from include.ReadData import *
from include.Merge import *
## ---------------------------- ##

def RemoveBg(dataFile):

    """
    Function that removes the background rate of a spectrum, using the
    Backgroud measurement data.

    INPUTS: 
    OUTPUTS: 
    """

    print('Removing background from file: ', dataFile)

    ##############################
    ## Get calibration run rate ##
    ##############################
    ## Check detector HPGe or SDD from file name
    if "HPGe" in dataFile:        
        calibYield, _, acquiTime = Ge2Lists(dataFile)
        ##############################
        ## Get background runs rate ##
        ##############################
        ## Background runs path
        bgPath = '../Calibrations/HPGe/Background/'

        ## Merge background yield
        mergeBgYield = Merge(bgPath, 'ge')

        ## Background acquisition time
        bgTime = 35*1800 + 777 ## seconds: 35 full runs * 1800 sec each + 777 sec last run

    elif "SDD" in dataFile:
        calibYield, _, acquiTime = MCA2Lists(dataFile)
        ##############################
        ## Get background runs rate ##
        ##############################
        ## Background runs path
        bgPath = '../Calibrations/SDD/Background/'

        ## Merge background yield
        mergeBgYield = Merge(bgPath, 'sdd')

        ## Background acquisition time
        bgTime = 45954 ## seconds
        
    ## Converts histogram counts to rate
    calibRate = [calibYield[i]/acquiTime for i in range(len(calibYield))]

    ## Set Energy axes
    ch_hpge = [(i+1) for i in range(4096)]
    ch_sdd = [(i+1) for i in range(2048)]

    ## Set label
    #lab = 'MUDAR'

    ## Background rate
    bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]
    
    ## Set label
    #bgLab = 'Background Rate'

    ######################################
    ## Remove background rate from file ##
    ######################################
    calibRateBgRem = [(calibRate[i] - bgRate[i]) for i in range(len(calibRate))]

    ## Set label
    #rateLab = 'Run10_152Eu-8mm - BG removed'

    ########################################################
    ## Plot both calib, bg rate and calib with bg removed ##
    ########################################################
    #Plot3RateLogy(ch_sdd, calibRate, bgRate, calibRateBgRem, lab, bgLab, rateLab)

    ##################################################################
    ## Save calibration rate with background removed values to file ##
    ##################################################################
    with open(dataFile.replace(".mca","_BgRemoved.mca"), 'w') as outFile:
        counts = 0
        for rate in calibRateBgRem:
            if rate <= 0:
                outFile.write(f"{counts:.0f}\n")
            elif rate > 0:
                counts = int(rate * acquiTime)      ## convert count rate back to counts
                outFile.write(f"{counts:.0f}\n")
    outFile.close()

    return str(f"New file {dataFile}_BgRemoved.mca writen \n")

sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/',]

for path in sddPaths:
    for file in os.listdir(path):
        RemoveBg(str(path+file))