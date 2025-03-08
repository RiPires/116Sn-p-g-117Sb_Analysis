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
    int_Ka = 0.
    accu_Kb = 0.
    int_Kb = 0.
    accu_g = 0.
    int_g = 0.
    accu_511 = 0.
    accu_t = 0.

    ## Set empty lists to store accumulation points and time
    Accu_Ka = []
    Integral_Ka = []
    Accu_Kb = []
    Integral_Kb = []
    Accu_g = []
    Integral_g = []
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
        #print(f"{file}\n")
        y = Ge2ListsBgRm(str(gePath+file))[0]
        ## Add Ka counts
        for c in range(roiDown_Ka, roiUp_Ka):
            accu_Ka += y[c]
            accu_Ka_err = np.sqrt(accu_Ka)
            
        ## Perform Gauss fit for Ka peak
        popt_Ka, pcov_Ka = curve_fit(gaussian, ch[roiDown_Ka:roiUp_Ka+1], 
                                     y[roiDown_Ka:roiUp_Ka+1], p0=[100, 80, 2])
        # Extract fitting parameters and their uncertainties
        amp_Ka, mean_Ka, sigma_Ka = popt_Ka
        amp_Ka_err, mean_Ka_err, sigma_Ka_err = np.sqrt(np.diag(pcov_Ka))
        
        # Print the results
        #print(f"Fitting Parameters:")
        #print(f"amp = {amp_Ka:.4f} ± {amp_Ka_err:.4f}")
        #print(f"mean = {mean_Ka:.4f} ± {mean_Ka_err:.4f}")
        #print(f"sigma_Ka = {sigma_Ka:.4f} ± {sigma_Ka_err:.4f}\n")

        # Plot the results
        ch_fit_Ka = np.linspace(ch[roiDown_Ka], ch[roiUp_Ka], 500)  # Fine grid for plotting
        y_fit_Ka = gaussian(ch_fit_Ka, *popt_Ka)

        #print(f"Integral = {trapz(y_fit, ch_fit):.3e}")
        #print(f"Accumulation = {accu_Ka:.3e}")

        int_Ka += trapz(y_fit_Ka, ch_fit_Ka)

        #fig, ax = plt.subplots()
        #ax.set_yscale("log")
        #ax.errorbar(ch, y, yerr=np.sqrt(y), color='blue', fmt='*-', label="Decay Aquisition")
        #ax.plot(ch_fit, y_fit, color='red', label="Peak Gaussian fit")
        #legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
        #legend.get_frame().set_facecolor('#DAEBF2')
        #tick_params(axis='both', which='major', labelsize=22)
        #xlabel("Channel", fontsize=22)
        #ylabel("Yield", fontsize=22)
        #show()

        ## Add Kb counts
        for c in range(roiDown_Kb, roiUp_Kb):
            accu_Kb += y[c]
            accu_Kb_err = np.sqrt(accu_Kb)

        try:
            ## Perform Gauss fit for Kb peak
            popt_Kb, pcov_Kb = curve_fit(gaussian, ch[roiDown_Kb:roiUp_Kb+1], 
                                        y[roiDown_Kb:roiUp_Kb+1], p0=[max(y[roiDown_Kb:roiUp_Kb+1]), 90, 2])
            # Extract fitting parameters and their uncertainties
            amp_Kb, mean_Kb, sigma_Kb = popt_Kb
            amp_Kb_err, mean_Kb_err, sigma_Kb_err = np.sqrt(np.diag(pcov_Kb))
            
            # Print the results
            #print(f"Fitting Parameters:")
            #print(f"amp = {amp_Kb:.4f} ± {amp_Kb_err:.4f}")
            #print(f"mean = {mean_Kb:.4f} ± {mean_Kb_err:.4f}")
            #print(f"sigma_Ka = {sigma_Kb:.4f} ± {sigma_Kb_err:.4f}\n")

            # Plot the results
            ch_fit_Kb = np.linspace(ch[roiDown_Kb], ch[roiUp_Kb], 500)  # Fine grid for plotting
            y_fit_Kb = gaussian(ch_fit_Kb, *popt_Kb)

            #print(f"Integral = {trapz(y_fit_Kb, ch_fit_Kb):.3e}")
            #print(f"Accumulation = {accu_Kb:.3e}")

            int_Kb += trapz(y_fit_Kb, ch_fit_Kb)

            #fig, ax = plt.subplots()
            #ax.set_yscale("log")
            #ax.errorbar(ch, y, yerr=np.sqrt(y), color='blue', fmt='*-', label="Decay Aquisition")
            #ax.plot(ch_fit_Kb, y_fit_Kb, color='red', label="Peak Gaussian fit")
            #legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
            #legend.get_frame().set_facecolor('#DAEBF2')
            #tick_params(axis='both', which='major', labelsize=22)
            #xlabel("Channel", fontsize=22)
            #ylabel("Yield", fontsize=22)
            #show()
        except RuntimeError:
            #print(f"Unable to fit peak. Changing to sum method.")
            for c in range(roiDown_Kb, roiUp_Kb):
                int_Kb += y[c]


        ## Add gamma counts
        for c in range(roiDown_g, roiUp_g):
            accu_g += y[c]
            accu_g_err = np.sqrt(accu_g)

        try:
            ## Perform Gauss fit for gamma peak
            popt_g, pcov_g = curve_fit(gaussian, ch[roiDown_g:roiUp_g+1], 
                                        y[roiDown_g:roiUp_g+1], p0=[100, 495, 2])
            # Extract fitting parameters and their uncertainties
            amp_g, mean_g, sigma_g = popt_g
            amp_g_err, mean_g_err, sigma_g_err = np.sqrt(np.diag(pcov_g))
            
            # Print the results
            #print(f"Fitting Parameters:")
            #print(f"amp = {amp_g:.4f} ± {amp_g_err:.4f}")
            #print(f"mean = {mean_g:.4f} ± {mean_g_err:.4f}")
            #print(f"sigma_Ka = {sigma_g:.4f} ± {sigma_g_err:.4f}\n")

            # Plot the results
            ch_fit_g = np.linspace(ch[roiDown_g], ch[roiUp_g], 500)  # Fine grid for plotting
            y_fit_g = gaussian(ch_fit_g, *popt_g)

            #print(f"Integral = {trapz(y_fit_g, ch_fit_g):.3e}")
            #print(f"Accumulation = {accu_g:.3e}")

            int_g += trapz(y_fit_g, ch_fit_g)

            #fig, ax = plt.subplots()
            #ax.set_yscale("log")
            #ax.errorbar(ch, y, yerr=np.sqrt(y), color='blue', fmt='*-', label="Decay Aquisition")
            #ax.plot(ch_fit_g, y_fit_g, color='red', label="Gamma Peak Gaussian fit")
            #ax.plot(ch_fit_Ka, y_fit_Ka, color='orange', label='Ka peak gaussian fit')
            #ax.plot(ch_fit_Kb, y_fit_Kb, color='green', label='Kb peak gaussian fit')
            #legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
            #legend.get_frame().set_facecolor('#DAEBF2')
            #tick_params(axis='both', which='major', labelsize=22)
            #xlabel("Channel", fontsize=22)
            #ylabel("Yield", fontsize=22)
            #show()

        except RuntimeError:
            #print(f"Unable to fit peak. Changing to sum method.")
            for c in range(roiDown_g, roiUp_g):
                int_g += y[c]

        ## Add 511 keV counts
        for c in range(roiDown_511, roiUp_511):
            accu_511 += y[c]
        ## Increment time
        accu_t += 15 # minutes
        ## Save integral at this point
        Accu_Ka.append(accu_Ka)
        Integral_Ka.append(int_Ka)
        Accu_Ka_err.append(accu_Ka_err)
        Accu_Kb.append(accu_Kb)
        Integral_Kb.append(int_Kb)
        Accu_Kb_err.append(accu_Kb_err)
        Accu_g.append(accu_g)
        Integral_g.append(int_g)
        Accu_g_err.append(accu_g_err)
        Accu_511.append(accu_511)
        Accu_t.append(accu_t)

    return Accu_Ka, Integral_Ka, Accu_Ka_err, Accu_Kb, Integral_Kb, Accu_Kb_err, Accu_g, Integral_g, Accu_g_err, Accu_511, Accu_t


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