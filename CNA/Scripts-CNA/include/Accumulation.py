#############################  RiP  ###################################
###   Functions to perform the accumulation of decay measurements   ###
#######################################################################

## ------------------ ##
import os
from include.ReadData import *
from include.Merge import *
## ------------------ ##

#######################################################################
#######################################################################
def AccumulateGe(gePath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: gePath - the path for the directory containing the decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated yield for Ka, Kb, and gamma lines, and time
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
    Performs Accumulation of the decay runs of a specific path removing the background

    INPUTS: gePath - the path for the directory containing the decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated yield for Ka, Kb, and gamma lines, and time
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

    ## 511 keV
    roiDown_511 = int(1577)
    roiUp_511 = int(1594)

    ## Loop over Ge data
    for file in os.listdir(gePath):
        y = Ge2ListsBgRm(str(gePath+file))[0]
        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
        ## Add gamma counts
        for c in range(roiDown_g, roiUp_g):
            accu_g += y[c]
        ## Add 511 keV counts
        for c in range(roiDown_511, roiUp_511):
            accu_511 += y[c]
        ## Increment time
        accu_t += 15 # minutes
        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Kb.append(accu_Kb)
        Accu_g.append(accu_g)
        Accu_511.append(accu_511)
        Accu_t.append(accu_t)
    return Accu_Ka, Accu_Kb, Accu_g, Accu_511, Accu_t


#######################################################################
#######################################################################
def AccumulateSDD(sddPath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: sddPath - the path for the directory containing the decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated yield for Ka, Kb, and gamma lines, and time
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

    INPUTS: sddPath - the path for the directory containing the decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated yield for Ka, Kb, and gamma lines, and time
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