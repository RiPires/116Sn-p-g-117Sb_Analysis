###############################################
## Script for calculation of SDD calibration ##
#  peak centroids, and sigmas                ##
###############################################

"""
Script for fitting SDD calibration runs' peaks
 returning mean value and standard deviation for further energy
 and resolution calibration
"""

## ---------------------------- ##
from include.Fits import*
## ---------------------------- ##



def FitPeak_SDD(y, lab, rois):
    
    initial_guess = [
    #   amp,  mean, sigma
        1000, 800, 2.0,   # Ka peak
        500,  915, 3.0]   # Kb peak
    
    ch = [(i+1) for i in range(2048)]


    

    return FitData(gaussian, ch, y, initial_guess, lab, rois)

##  Fit the data usign single peak fit
FitData(gaussian, channels, calibYield152Eu, initial_guess152Eu, lab152Eu, ROId152Eu, ROIu152Eu)
FitData(gaussian, channels, calibYield133Ba, initial_guess133Ba, lab133Ba, ROId133Ba, ROIu133Ba)

## Fit data using multi-peak fit
FitNGauss(nGaussian, channels, calibYield152Eu, initial_guess152Eu, lab152Eu)
FitNGauss(nGaussian, channels, calibYield133Ba, initial_guess133Ba, lab133Ba)