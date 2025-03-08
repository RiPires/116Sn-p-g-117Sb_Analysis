#############################  RiP  ###################################
###   Functions to perform the accumulation of decay measurements   ###
#######################################################################

## ------------------ ##
import os
from include.ReadData import *
from include.Merge import *
from include.Fits import *
import numpy as np
from scipy.integrate import simps
from scipy.optimize import curve_fit
## ------------------ ##

#######################################################################
#######################################################################
def AccumulateGe(gePath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: gePath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of 
    accumulated yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka = 0.
    accu_Kb = 0.
    accu_g = 0.
    accu_t = 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka = []
    Accu_Kb = []
    Accu_g = []
    Accu_t = []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(74)
    roiUp_Ka = int(84)

    ## Kb
    roiDown_Kb = int(86)
    roiUp_Kb = int(94)

    ## gamma
    roiDown_g = int(488)
    roiUp_g = int(498)

    ## Loop over Ge data
    for file in os.listdir(gePath):
        y = Ge2Lists(str(gePath+file))[0]
        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
        for c in range(roiDown_g, roiUp_g):
            accu_g += y[c]
        ## Increment time
        accu_t += 15 # minutes
        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Kb.append(accu_Kb)
        Accu_g.append(accu_g)
        Accu_t.append(accu_t)
    return Accu_Ka, Accu_Kb, Accu_g, Accu_t


#######################################################################
#######################################################################
def AccumulateGe_BgRemove(gePath):
    """
    Performs Accumulation of the decay runs of a specific path 
    removing the background

    INPUTS: gePath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated 
    yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka = 0.
    accu_Kb = 0.
    accu_g = 0.
    accu_511 = 0.
    accu_t = 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka = []
    Accu_Kb = []
    Accu_g = []
    Accu_511 = []
    Accu_t = []

    ## Set channels list
    ch = [(i+1) for i in range(4096)]

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(72)
    roiUp_Ka = int(84)

    ## Kb
    roiDown_Kb = int(84)
    roiUp_Kb = int(94)

    ## gamma
    roiDown_g = int(486)
    roiUp_g = int(498)

    ## 511 keV
    roiDown_511 = int(1577)
    roiUp_511 = int(1594)

    Accu_Ka_err, Accu_Kb_err, Accu_g_err = [0], [0], [0]

    ## Loop over Ge data
    for file in sorted(os.listdir(gePath)):

        y = Ge2ListsBgRm(str(gePath+file))[0]

        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
            accu_Ka_err = np.sqrt(accu_Ka)
            
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
            accu_Kb_err = np.sqrt(accu_Kb)

        ## Add gamma counts
        for c in range(roiDown_g, roiUp_g):
            accu_g += y[c]
            accu_g_err = np.sqrt(accu_g)

        ## Add 511 keV counts
        for c in range(roiDown_511, roiUp_511):
            accu_511 += y[c]

        ## Increment time
        accu_t += 15 # minutes

        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_g.append(accu_g)
        Accu_g_err.append(accu_g_err)
        Accu_511.append(accu_511)
        Accu_t.append(accu_t)

    return Accu_Ka, Accu_Ka_err, Accu_Kb, Accu_Kb_err, Accu_g, Accu_g_err, Accu_511, Accu_t

#######################################################################
#######################################################################
def AccumulateSDD(sddPath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: sddPath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated 
    yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka = 0.
    accu_Kb = 0.
    accu_t = 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka = []
    Accu_Kb = []
    Accu_t = []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(796)
    roiUp_Ka = int(827)

    ## Kb
    roiDown_Kb = int(907)
    roiUp_Kb = int(928)

    ## Loop over Ge data
    for file in os.listdir(sddPath):
        y = MCA2Lists(str(sddPath+file))[0]
        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
        ## Increment time
        accu_t += 30 # minutes
        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Kb.append(accu_Kb)
        Accu_t.append(accu_t)

    return Accu_Ka, Accu_Kb, Accu_t

#######################################################################
#######################################################################
def AccumulateSDD_BgRemoved(sddPath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: sddPath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated 
    yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka = 0.
    accu_Kb = 0.
    accu_t = 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka = []
    Accu_Kb = []
    Accu_t = []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(802)
    roiUp_Ka = int(822)

    ## Kb
    roiDown_Kb = int(911)
    roiUp_Kb = int(925)

    ## Loop over Ge data
    for file in os.listdir(sddPath):
        y = MCA2ListsBgRm(str(sddPath+file))[0]
        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
        ## Increment time
        accu_t += 30 # minutes
        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Kb.append(accu_Kb)
        Accu_t.append(accu_t)

    return Accu_Ka, Accu_Kb, Accu_t