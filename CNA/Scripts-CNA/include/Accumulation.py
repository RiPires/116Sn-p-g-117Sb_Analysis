#############################  RiP  ###################################
###   Functions to perform the accumulation of decay measurements   ###
#######################################################################

## ------------------ ##
import os
from include.ReadData import *
from include.Fits import *
import numpy as np
from scipy.integrate import simps
from scipy.optimize import curve_fit
## ------------------ ##

## ************************************************* ##
## Function to perform accumulation of raw HPGe data ##
## ************************************************* ##
def AccumulateGe(gePath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: gePath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of 
    accumulated yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka, accu_Kb, accu_g, accu_511, accu_t = 0., 0., 0., 0., 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka, Accu_Kb, Accu_g, Accu_511, Accu_t = [0], [0], [0], [0], []

    ## Set channels list
    ch = [(i+1) for i in range(4096)]

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(71)
    roiUp_Ka = int(85)

    ## Kb
    roiDown_Kb = int(86)
    roiUp_Kb = int(96)

    ## gamma
    roiDown_g = int(486)
    roiUp_g = int(501)

    ## 511 keV
    roiDown_511 = int(1571)
    roiUp_511 = int(1602)

    Accu_Ka_err, Accu_Kb_err, Accu_g_err, Accu_511_err = [0], [0], [0], [0]
    counter = 1

    ## Loop over Ge data files
    for file in sorted(os.listdir(gePath)):

        ## Get run yield and live time
        y, _, live_time = Ge2Lists(str(gePath+file))
        #print(f"live-time = {live_time:.0f} s = {live_time/60:.1f} min")

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
            accu_511_err = np.sqrt(accu_511 + Accu_511[counter-1])

        ## Increment accumulation time and counter
        accu_t += live_time/60 # minutes
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
        Accu_511_err.append(accu_511_err)
        Accu_t.append(accu_t)

    return Accu_Ka[1:], Accu_Ka_err, Accu_Kb[1:], Accu_Kb_err, Accu_g[1:], Accu_g_err, Accu_511[1:], Accu_511_err, Accu_t

## ************************************************* ##
## Function to perform accumulation of HPGe data     ##
## after background removed                          ##
## ************************************************* ##
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
    accu_Ka, accu_Kb, accu_g, accu_511, accu_861, accu_1004, accu_t = 0., 0., 0., 0., 0., 0., 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka, Accu_Kb, Accu_g, Accu_511, Accu_861, Accu_1004, Accu_t = [0], [0], [0], [0], [0], [0], []

    ## Set lists for accumulation error and counter
    Accu_Ka_err, Accu_Kb_err, Accu_g_err, Accu_511_err, Accu_861_err, Accu_1004_err = [0], [0], [0], [0], [0], [0]
    counter = 1

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(62)
    roiUp_Ka   = int(88)

    ## Kb
    roiDown_Kb = int(86)
    roiUp_Kb   = int(96)

    ## gamma
    roiDown_g = int(483)
    roiUp_g   = int(503)

    ## 511 keV
    roiDown_511 = int(1571)
    roiUp_511   = int(1602)

    ## 861 keV
    roiDown_861 = int(2660)
    roiUp_861   = int(2684)

    ## 1004 keV
    roiDown_1004 = int(3102)
    roiUp_1004   = int(3126)

    ## Loop over Ge data files
    for file in sorted(os.listdir(gePath)):

        ## Get run yield and live time
        y = Ge2ListsBgRm(str(gePath+file))[0]
        #live_time = Ge2Lists(str(gePath.replace("BgRemoved_LiveTime/","")+file.replace("_BgRemoved","")))[2]

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
            accu_511_err = np.sqrt(accu_511 + Accu_511[counter-1])

        ## Add 861 keV counts
        for c in range(roiDown_861, roiUp_861):
            accu_861 += y[c]
            accu_861_err = np.sqrt(accu_861 + Accu_861[counter-1])

        ## Add 1004 keV counts
        for c in range(roiDown_1004, roiUp_1004):
            accu_1004 += y[c]
            accu_1004_err = np.sqrt(accu_1004 + Accu_1004[counter-1])

        ## Increment accumulation time and counter
        accu_t += 15. # minutes
        counter += 1

        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_g.append(accu_g)
        Accu_g_err.append(accu_g_err)
        Accu_511.append(accu_511)
        Accu_511_err.append(accu_511_err)
        Accu_861.append(accu_861)
        Accu_861_err.append(accu_861_err)
        Accu_1004.append(accu_1004)
        Accu_1004_err.append(accu_1004_err)
        Accu_t.append(accu_t)

    return Accu_Ka[1:], Accu_Ka_err, Accu_Kb[1:], Accu_Kb_err, Accu_g[1:], Accu_g_err, Accu_511[1:], Accu_511_err, Accu_861[1:], Accu_861_err, Accu_1004[1:], Accu_1004_err, Accu_t

## ************************************************* ##
## Function to perform accumulation of raw SDD data  ##
## ************************************************* ##
def AccumulateSDD(sddPath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: sddPath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated 
    yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka, accu_Kb, accu_t = 0., 0., 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka, Accu_Ka_err, Accu_Kb, Accu_Kb_err, Accu_t = [0], [0], [0], [0], []

    ## Set ROI for each peak, in channel
    ## Ka
    roiDown_Ka = int(802)
    roiUp_Ka = int(822)

    ## Kb
    roiDown_Kb = int(911)
    roiUp_Kb = int(925)

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

## ************************************************* ##
## Function to perform accumulation of SDD data      ##
## after background removed                          ##
## ************************************************* ##
def AccumulateSDD_BgRemoved(sddPath):
    """
    Performs Accumulation of the decay runs of a specific path

    INPUTS: sddPath - the path for the directory containing the 
    decay data files

    OUPUTS: Accu_Ka, Accu_Kb, Accu_g, Accu_t - lists of accumulated 
    yield for Ka, Kb, and gamma lines, and time
    """
    ## Set accumulation and time as zero
    accu_Ka, accu_Kb, accu_L, accu_t = 0., 0., 0., 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka, Accu_Ka_err, Accu_Kb, Accu_Kb_err, Accu_L, Accu_L_err, Accu_t = [0], [0], [0], [0], [0], [0], []
    counter = 1

    ## Set ROI for each peak, in channel
    ## Ka1,2 lines
    roiDown_Ka = int(797)
    roiUp_Ka   = int(825)

    ## Kb1,3 lines
    roiDown_Kb = int(909)
    roiUp_Kb   = int(927)

    ## L- lines
    roiDown_L = int(105)
    roiUp_L = int(135)

    ## Loop over SDD runs
    for file in sorted(os.listdir(sddPath)):

        ## Get run yield background removed and run live time
        y = MCA2ListsBgRm(str(sddPath+file))[0]

        ## Perform Ka accumulation summing channel by channel
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
            accu_Ka_err = np.sqrt(accu_Ka + Accu_Ka[counter-1])

        ## Perform Kb accumulation
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
            accu_Kb_err = np.sqrt(accu_Kb + Accu_Kb[counter-1]) 

        ## Perform L-lines accumulation
        for c in range(roiDown_L, roiUp_L):
            accu_L += y[c]
            accu_L_err = np.sqrt(accu_L + Accu_L[counter-1])

        ## Increment time
        accu_t += 30 # minutes
        counter += 1

        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_L.append(accu_L)
        Accu_L_err.append(accu_L_err)
        Accu_t.append(accu_t)

    return Accu_Ka[1:], Accu_Ka_err, Accu_Kb[1:], Accu_Kb_err, Accu_L[1:], Accu_L_err, Accu_t