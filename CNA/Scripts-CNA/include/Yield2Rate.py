#################### RiP ##############################
## Script for converting count yield into count rate ##
#######################################################

## ---------------------------- ##
from ReadData import *
## ---------------------------- ##

def Yield2Rate(dataFile, acquTime, save):
    
    """
    EXPLANATION

    INPUTS:
    OUTPUTS:
    """

    ## Check detector HPGe or SDD from file name
    if "HPGe" in dataFile:        
        dataYield = Ge2Lists(dataFile)[0]
        print('HPGe')
    elif "SDD" in dataFile:
        dataYield = MCA2Lists(dataFile)[0]
        print('HPGe')

    print(dataYield)
    ## Converts histogram counts to rate
    calibRate = [dataYield[i]/acquTime for i in range(len(dataYield))]

    if save:
        with open(dataFile+"_BgRemoved.mca", 'w') as outFile:
            for value in dataYield:
                outFile.write(f"{value:.2f}\n") ## value back to counts instead of count rate
        outFile.close()

    return calibRate

Yield2Rate('../../Calibrations/HPGe/Background/Background_HPGe_001.mca', "b", True)