#################### RiP ###########################
## Script for removing background from the 152Eu  ##
## calibration run                                ##
####################################################

## ---------------------------- ##
from include.PlotData import *
from include.ReadData import *
from include.Merge import *
## ---------------------------- ##


def RemoveBg(dataFile, acquTime):

    """
    Function that removes the background rate of a spectrum, using the
    Backgroud measurement data.

    INPUTS: 
    OUTPUTS: 
    """

    ##############################
    ## Get calibration run rate ##
    ##############################
    ## Check detector HPGe or SDD from file name
    if "HPGe" in dataFile:        
        calibYield = Ge2Lists(dataFile)[0]
    elif "SDD" in dataFile:
        calibYield = MCA2Lists(dataFile)[0]

    ## Converts histogram counts to rate
    calibRate = [calibYield[i]/acquTime for i in range(len(calibYield))]

    ## Set Energy axes
    ch_hpge = [((i+1)*0.3225-0.149) for i in range(4096)] ## ALWAYS check for CALIBRATION parameters

    ## Set label
    lab = 'MUDAR'

    ## Plot rate
    #PlotRateLogy(ch_hpge, calibRate, lab)

    ##############################
    ## Get background runs rate ##
    ##############################
    ## Background runs path
    bgPath = '../Calibrations/HPGe/Background/'

    ## Merge background yield
    mergeBgYield = Merge(bgPath, 'ge')

    ## Background acquisition time
    bgTime = 35*1800 + 777 ## seconds: 35 full runs * 1800 sec each + 777 sec last run

    ## Background rate
    bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]

    ## Set label
    bgLab = 'Background Rate'

    ## Plot bg rate
    #PlotRateLogy(ch_hpge, bgRate, bgLab)

    ##############################
    ## Plot both calib and bg rate
    ##############################
    #PlotBothRateLogy(ch_hpge, calibRate, bgRate, lab, bgLab)

    ######################################
    ## Remove background rate from file ##
    ######################################
    calibRateBgRem = [(calibRate[i] - bgRate[i]) for i in range(len(calibRate))]

    ## Set label
    rateLab = 'Run10_152Eu-8mm-BG removed'

    ## Plot calib rate bg removed
    #PlotRateLogy(ch_hpge, calibRateBgRem,rateLab)

    ########################################################
    ## Plot both calib, bg rate and calib with bg removed ##
    ########################################################
    Plot3RateLogy(ch_hpge, calibRate, bgRate, calibRateBgRem, lab, bgLab, rateLab)

    ##################################################################
    ## Save calibration rate with background removed values to file ##
    ##################################################################
    with open(dataFile+"_BgRemoved.mca", 'w') as outFile:
        for value in calibRateBgRem:
            outFile.write(f"{value:.2f}\n") ## value back to counts instead of count rate
    outFile.close()

    return