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
    if "Ge" in dataFile:  

        ## Data to remove background     
        dataYield = Ge2Lists(dataFile)[0]
        acquiTime = 15 * 60 # s = 15 minutes

        ## Background run path
        bgFile = '../Calibration/BEGe-Calib/Background/415114G2.TXT'
        bgYield = Ge2Lists(bgFile)[0]
        ## Background acquisition time
        bgTime = 64 * 60 + 9 # s = 1h 4m 9s
        
    elif "SDD" in dataFile:
        dataYield, _, acquiTime = MCA2Lists(dataFile)
        ## Background runs path
        bgPath = '../Calibrations/SDD/Background/'
        ## Merge background yield
        mergeBgYield = Merge(bgPath, 'sdd')
        ## Background acquisition time
        bgTime = 45954 ## seconds
        acquiTime = 15 * 60 # s = 15 minutes
    
    ## Converts data counts to count rate (in s^-1)
    dataRate = [dataYield[i]/acquiTime for i in range(len(dataYield))]
    ## Converts background counts to background count rate (in s^-1)
    bgRate = [bgYield[i]/bgTime for i in range(len(bgYield))]
    ## Remove background rate from file 
    calibRateBgRem = [(dataRate[i] - bgRate[i]) for i in range(len(dataRate))]

    ## Set Energy axes
    ch_hpge = [(i+1) for i in range(1024)]
    ch_sdd = [(i+1) for i in range(2048)]

    ## Set label
    lab = dataFile[-63:-51] + ': ' + dataFile[-26:-4]
    ## Set label
    bgLab = 'Background Rate'
    ## Set label
    rateLab = lab +'_BG removed'
    ## Background rate

    ## Plot both calib, bg rate and calib with bg removed 
    #Plot3RateLogy(ch_hpge, dataRate, bgRate, calibRateBgRem, lab, bgLab, rateLab)

    ## Save calibration rate with background removed values to file 
    with open(dataFile.replace(".TXT","_BgRemoved.TXT"), 'w') as outFile:
        counts = 0
        outFile.write(dataFile+"BackgroundRemoved \n")
        for rate in calibRateBgRem:
            if rate <= 0:
                outFile.write(f"{counts:.0f}\n")
            elif rate > 0:
                counts = int(rate * acquiTime)      ## convert count rate back to counts
                outFile.write(f"{counts:.0f}\n")
    outFile.close()

    return

##  ***********************************************************  ##
##               Perform background removal here                 ##
##  ***********************************************************  ##

## For specific data file
#filePath = '../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/116Sn-C3_Decay_HPGe-089.mca'
#RemoveBg(filePath)

## Remove background for every data file
gePath = '../2_Decay/DataFilesGe/Decay/'
for file in sorted(os.listdir(gePath)):
    RemoveBg(str(gePath+file))