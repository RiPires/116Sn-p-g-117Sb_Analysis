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
    roiDown_Ka = int(36)
    roiUp_Ka = int(38)

    ## Kb
    roiDown_Kb = int(39)
    roiUp_Kb = int(42)

    ## gamma
    roiDown_g = int(161)
    roiUp_g = int(165)

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
    Accu_Ka = [0]
    Accu_Kb = [0]
    Accu_g = [0]
    Accu_511 = []
    Accu_t = []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(36)
    roiUp_Ka = int(38)

    ## Kb
    roiDown_Kb = int(39)
    roiUp_Kb = int(42)

    ## gamma
    roiDown_g = int(161)
    roiUp_g = int(165)

    ## 511 keV
    roiDown_511 = int()
    roiUp_511 = int()

    Accu_Ka_err, Accu_Kb_err, Accu_g_err = [0], [0], [0]
    counter = 1

    ## Loop over Ge data files with bg removed
    for file in sorted(os.listdir(gePath)):

        y = Ge2Lists(str(gePath+file))[0]

        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
            accu_Ka_err = np.sqrt(accu_Ka + Accu_Ka[counter-1])
            
        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
            accu_Kb_err = np.sqrt(accu_Kb + Accu_Kb[counter-1])

        ## Add gamma counts
        for c in range(roiDown_g, roiUp_g):
            accu_g += y[c]
            accu_g_err = np.sqrt(accu_g + Accu_g[counter-1])

        ## Add 511 keV counts
        for c in range(roiDown_511, roiUp_511):
            accu_511 += y[c]

        ## Increment accumulation time and counter
        accu_t += 15 # minutes
        #print(f"Acumulation time = {accu_t:.0f} min \n")
        counter += 1

        #print(f"Ratio Ka/Kb yields = {accu_Ka/accu_Kb:.2f}")

        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_g.append(accu_g)
        Accu_g_err.append(accu_g_err)
        Accu_511.append(accu_511)
        Accu_t.append(accu_t)

    return Accu_Ka[1:], Accu_Ka_err, Accu_Kb[1:], Accu_Kb_err, Accu_g[1:], Accu_g_err, Accu_511, Accu_t

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
    Accu_Ka = [0]
    Accu_Kb = [0]
    Accu_t = []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(793)
    roiUp_Ka = int(830)

    ## Kb
    roiDown_Kb = int(906)
    roiUp_Kb = int(927)

    Accu_Ka_err, Accu_Kb_err = [0], [0]
    counter = 1

    ## Loop over SDD data files
    for file in sorted(os.listdir(sddPath)):

        y = MCA2Lists(str(sddPath+file))[0]
        live_time = MCA2Lists(str(sddPath+file))[2]
        #print(f"Live-time = {live_time:.0f} s = {live_time/60:.1f} min")

        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
            accu_Ka_err = np.sqrt(accu_Ka + Accu_Ka[counter-1])

        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
            accu_Kb_err = np.sqrt(accu_Kb + Accu_Kb[counter-1])

        ## Increment accumulation time and counter
        accu_t += live_time/60 # minutes
        #print(f"Accumulation time = {accu_t:.0f} min \n")
        counter += 1

        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_t.append(accu_t)

    return Accu_Ka[1:], Accu_Ka_err[1:], Accu_Kb[1:], Accu_Kb_err[1:], Accu_t

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