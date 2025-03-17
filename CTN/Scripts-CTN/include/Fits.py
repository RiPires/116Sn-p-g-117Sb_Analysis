#################### RiP ########################
## Funtions to fit theorethical curves to data ##
#################################################

## ------------------------------- ##
from __future__ import print_function 
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import numpy as np
from scipy.optimize import curve_fit
## ------------------------------- ##

## Define the Gaussian function
def gaussian(x, amp, mean, sigma):
    return amp * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))

## Fits function "func" to experimental data x and y, within certain regions of interest 
def FitData(func, x, y, init, lab, roid, roiu):
    
    """
    Uses scipy curve_fit to perform fit of a fucntion "func" to experimental data 
    x and y, given initial guesses "init", in the regions of interest limited 
    by roid and roiu.
    Writes the peak centroid and standard deviation into an output file with a costume 
    name given by the label "lab".
    Prints the results into the terminal.
    Plots both the data and the fit.

    INPUTS - func: fucntion to fit; x: x-data; y: y-data; init: initial guess 
    for fitting; lab: label for plot; roid: region of interest down; roiu: region 
    of interest up;
    OUTPUTS - list of fitted parameters;
    """
    
    x = np.array(x)
    y = np.array(y)
    roid = np.array(roid)
    roiu = np.array(roiu)

    fitted_params = []
    all_fits = np.zeros_like(x, dtype=float)  # To store the combined fit for the full spectrum

    # Open file for output results
    fileName = f"GaussPeakAnalysis_{lab}.txt"
    with open(fileName, "w") as outFile:
        header = "Centroid\tSigma\n"
        outFile.write(header)
        # Loop over each ROI
        for i in range(len(roid)):
            # Restrict data to the ROI
            mask = (x >= roid[i]) & (x <= roiu[i])
            x_roi = x[mask]
            y_roi = y[mask]
            # Initial parameters for the current Gaussian
            p0 = init[3 * i: 3 * i + 3]
            # Fit the data within the ROI
            popt, pcov = curve_fit(func, x_roi, y_roi, p0=p0)
            fitted_params.append(popt)
            # Add current fit to the combined result
            all_fits += gaussian(x, *popt)
            # Extract uncertainty for sigma from the covariance matrix
            sigma_uncertainty = np.sqrt(np.diag(pcov))[2]  # Third parameter is sigma
            # Write results to file
            amp, mean, sigma = popt
            outFile.write(f"{mean:.2f}\t{sigma:.2f}\t{sigma_uncertainty:.2f}\n")
    outFile.close()

    # Print results
    print("*************************************"+len(lab)*"*")
    print("* Single peak gaussian fit results "+lab+"*")
    print("*************************************"+len(lab)*"*")
    for i, param in enumerate(fitted_params, start=1):
        print(f"Peak {i}: Amplitude = {param[0]:.2f}, Mean = {param[1]:.2f}, Sigma = {param[2]:.2f} ± {sigma_uncertainty:.2f}")
    print()

    # Plot the results
    fig, ax = plt.subplots()
    ax.plot(x, y, '+-', color="blue", label=f"Data ({lab})")
    ax.plot(x, all_fits, '--', color="red", label="Combined Fit")
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Channel", fontsize=22)
    ylabel("Yield", fontsize=22)
    title("Gaussian Fit")
    show()

    return fitted_params

#######################
## Accumulation fits ##
#######################

## Defines Accumulation function for the area under a photo-peak as N_peak(t_acqui) = \eta \epsilon_D exp(-lambda t_trans) N_Dirr (1-exp(-lamb t_acqui))
def NpeakBEGe(time, *params, radType):
    """
    Function that models the accumulation of radioactive decays over the acquisition time.

    INPUTS:
    time : ndarray
        The x-axis variable, time of acquisition.
    *params : tuple
        A flattened list of parameters for the function:
        - N_Dirr (int): total number of radioactive nuclei in the target after the irradiation and the transportation time.
        - lamb (float): the decay caracteristic time, depending on the radioactive decay.
        - eta (float): photo-peak decay branching;
        - epsilon_D (float): detector resolution at the photo-peak energy;
        - t_trans (float): time of transportation of the activated target, since the end of the activation,
          from the irradiation chamber, into the decay station at the begining of the decay measurement;

    OUPUTS: adjusted Npeak curve
    """    

    ## Efficiency and emission probabilities for each energy
    efficiency_params = {'gamma': (0.8590, 0.08082), 
                         'Ka':    (0.6750, 0.08246), 
                         'Kb':    (0.1419, 0.01817)}

    ## Transportation time (in minutes) for each activation energy
    t_transMin = 22. # minutes
    
    try:
        Ndirr = float(params[0])  # Force conversion to float
    except ValueError:
        raise TypeError(f"Expected a numeric value for Ndirr, but got {params[0]} (type: {type(params[0])})")

    time = np.asarray(time, dtype=np.float64)  # Ensure time is a NumPy array

    ## Get efficiency and emission probability for the given radiation type
    try:
        eta, epsilonD = efficiency_params[radType]
    except KeyError:
        raise ValueError(f"Invalid radType '{radType}'. Check input values.")

    ## Constants
    halfLifeMin = 2.8 * 60  # Decay half-life (minutes)
    lambda_decay = np.log(2) / halfLifeMin  # Decay constant

    ## Compute accumulation
    return eta * epsilonD * np.exp(-lambda_decay * t_transMin) * Ndirr * (1 - np.exp(-lambda_decay * time))

## Defines Accumulation function for the area under a photo-peak as N_peak(t_acqui) = \eta \epsilon_D exp(-lambda t_trans) N_Dirr (1-exp(-lamb t_acqui))
def NpeakSDD(time, *params, radType):
    """
    Function that models the accumulation of radioactive decays over the acquisition time.

    INPUTS:
    time : ndarray
        The x-axis variable, time of acquisition.
    *params : tuple
        A flattened list of parameters for the function:
        - N_Dirr (int): total number of radioactive nuclei in the target after the irradiation and the transportation time.
        - lamb (float): the decay caracteristic time, depending on the radioactive decay.
        - eta (float): photo-peak decay branching;
        - epsilon_D (float): detector resolution at the photo-peak energy;
        - t_trans (float): time of transportation of the activated target, since the end of the activation,
          from the irradiation chamber, into the decay station at the begining of the decay measurement;

    OUPUTS: adjusted Npeak curve
    """    

    ## Efficiency and emission probabilities for each energy
    efficiency_params = {'Ka': (0.6750, 2.842e-3),
                         'Kb': (0.1419, 3.733e-4)}

    ## Transportation time (in minutes) for each activation energy
    t_transMin = 15. # minutes
    
    try:
        Ndirr = float(params[0])  # Force conversion to float
    except ValueError:
        raise TypeError(f"Expected a numeric value for Ndirr, but got {params[0]} (type: {type(params[0])})")

    time = np.asarray(time, dtype=np.float64)  # Ensure time is a NumPy array

    ## Get efficiency and emission probability for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        eta, epsilonD = efficiency_params[radType]
    except KeyError:
        raise ValueError(f"Invalid radType '{radType}'. Check input values.")

    ## Constants
    halfLifeMin = 2.8 * 60  # Decay half-life (minutes)
    lambda_decay = np.log(2) / halfLifeMin  # Decay constant

    ## Compute accumulation
    return eta * epsilonD * np.exp(-lambda_decay * t_transMin) * Ndirr * (1 - np.exp(-lambda_decay * time))

## ************************************************************************************ ##
## Funtion to fit accumulation curve of area under a photo-peak to experimental data    ##
## extracting decay half-life (T_1/2), total nr. of radioactive nuclei at the end of    ##
## the activation (N_Dirr), decay branching ratio (eta), detector efficiency (epsilonD) ##
## and transportation time (t_trans), for the HPGe detector                             ##
## ************************************************************************************ ##
def FitNpeakBEGe(func, time, countsGamma, errGamma, countsKa, errKa, countsKb, errKb, init, lab):
    """
    INPUTS:
        - func: fucntion to fit;
        - time: acquisition time, the x-axis variable;
        - countsGamma: accumulation yield in counts, the y-axis variable, for the gamma line;
        - countsKa: accumulation yield in counts, the y-axis variable, for the Ka line;
        - countsKb: accumulation yield in counts, the y-axis variable, for the Kb line;
        - init: initial gusses for the fit parameters (N_Dirr, radType);
        - lab: a label to use for plotting;
    OUTPUTS:
    """

    ## Convert input arrays into numpy arrays
    time = np.array(time)
    countsGamma = np.array(countsGamma)
    countsKa = np.array(countsKa)
    countsKb = np.array(countsKb)

    ## Fit the data, passing radType explicitly
    poptGamma, pcovGamma = curve_fit(lambda t, *p: NpeakBEGe(t, *p, radType='gamma'), 
                                     time, countsGamma, p0=init[0][0:2])
    
    poptKa, pcovKa = curve_fit(lambda t, *p: NpeakBEGe(t, *p, radType='Ka'), 
                               time, countsKa, p0=init[1][0:2])
    
    poptKb, pcovKb = curve_fit(lambda t, *p: NpeakBEGe(t, *p, radType='Kb'), 
                               time, countsKb, p0=init[2][0:2])
    
    ## Get fit parameters and std_dev = sqrt(variance) = sqrt(diag(cov))
    NdirrGamma, NdirrGamma_err  = poptGamma[0], np.sqrt(np.diag(pcovGamma))[0]  # Gamma line
    NdirrKa, NdirrKa_err        = poptKa[0],    np.sqrt(np.diag(pcovKa))[0]     # Ka line
    NdirrKb, NdirrKb_err        = poptKb[0],    np.sqrt(np.diag(pcovKb))[0]     # Kb line

    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Gamma line: \t Ndirr = {NdirrGamma:.3e} +- {NdirrGamma_err:.0e}")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e}")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e}")
    print()

    ## Fit function for plotting
    fittedGamma = NpeakBEGe(time, *poptGamma, radType='gamma')
    fittedKa = NpeakBEGe(time, *poptKa, radType='Ka')
    fittedKb = NpeakBEGe(time, *poptKb, radType='Kb')

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.errorbar(time, countsGamma, yerr=errGamma[1:], fmt='*', color="xkcd:sky blue", label=f"Gamma")
    ax.semilogy(time, fittedGamma, '-', color="xkcd:blue", label="Fit - Gamma")
    ax.errorbar(time, countsKa, yerr=errKa[1:], fmt='^', color="xkcd:turquoise", label=f"Ka")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - Ka")
    ax.errorbar(time, countsKb, yerr=errKb[1:],fmt='v', color="xkcd:salmon", label=f"Kb")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - Kb")
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Time (minutes)", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit Npeak: "+lab, fontsize=24)
    show()

    return

## ************************************************************************************ ##
## Funtion to fit accumulation curve of area under a photo-peak to experimental data    ##
## extracting decay half-life (T_1/2), total nr. of radioactive nuclei at the end of    ##
## the activation (N_Dirr), decay branching ratio (eta), detector efficiency (epsilonD) ##
## and transportation time (t_trans), for the HPGe detector                             ##
## ************************************************************************************ ##
def FitNpeakSDD(func, time, countsKa, errKa, countsKb, errKb, init, lab):
    """
    INPUTS:
        - func: fucntion to fit;
        - time: acquisition time, the x-axis variable;
        - countsGamma: accumulation yield in counts, the y-axis variable, for the gamma line;
        - countsKa: accumulation yield in counts, the y-axis variable, for the Ka line;
        - countsKb: accumulation yield in counts, the y-axis variable, for the Kb line;
        - init: initial gusses for the fit parameters (N_Dirr, radType);
        - lab: a label to use for plotting;
    OUTPUTS:
    """

    ## Convert input arrays into numpy arrays
    time = np.array(time)
    countsKa = np.array(countsKa)
    countsKb = np.array(countsKb)

    ## Fit the data, passing radType explicitly    
    poptKa, pcovKa = curve_fit(lambda t, *p: NpeakSDD(t, *p, radType='Ka'), 
                               time, countsKa, p0=init[0:2])
    
    poptKb, pcovKb = curve_fit(lambda t, *p: NpeakSDD(t, *p, radType='Kb'), 
                               time, countsKb, p0=init[0:2])
    
    ## Get fit parameters
    NdirrKa, NdirrKa_err = poptKa[0], np.sqrt(np.diag(pcovKa))[0] # Ka line
    NdirrKb, NdirrKb_err = poptKb[0], np.sqrt(np.diag(pcovKb))[0] # Kb line

    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e}")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e}")
    print()

    ## Fit function for plotting
    fittedKa = NpeakSDD(time, *poptKa, radType='Ka')
    fittedKb = NpeakSDD(time, *poptKb, radType='Kb')

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.errorbar(time, countsKa, yerr=errKa, fmt='^', color="xkcd:turquoise", label=f"Ka")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - Ka")
    ax.errorbar(time, countsKb, yerr=errKb,fmt='v', color="xkcd:salmon", label=f"Kb")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - Kb")
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Time (minutes)", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit Npeak: "+lab, fontsize=24)
    show()

    return