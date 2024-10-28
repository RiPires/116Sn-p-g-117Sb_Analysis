#################### RiP ############################
## Funtion for analysing spectra using the FitData ##
## functions                                       ##
#####################################################

## ---------------------------- ##
from FitData import*
import numpy as np
## ---------------------------- ##

def Analyze(y, ROId, ROIu):

    """
    Function to analyse spectra peaks usign tge FitData
    functions ans returning peak centroid, error and sigmas.

    INPUTS: y - yield list; ROId - region of interest down list; ROIu - region of interest up list.

    OUTPUTS: centrois, error and sigmas lists. 
    """

    centroids = []
    sigmas = []
    error = []
    fwhm = []

    for r in range(len(ROId)):

        if ROId[r] == 0 or ROId[r] == '' or ROIu[r] == 0 or ROIu[r] == '':
            pass
        else:
            x1 = float(ROId[r])
            x2 = float(ROIu[r])

            Cent = peakCentroid(x1,x2,y)
            Sigma = peakSigma(x1,x2,y)
            Net = peakNet(x1,x2,y)
            FullWHM = peakFWHM(x1,x2,y)

            centroids.append(Cent)
            sigmas.append(Sigma)
            error.append(Sigma/np.sqrt(Net))
            fwhm.append(FullWHM)
            
    return centroids, error, sigmas, fwhm