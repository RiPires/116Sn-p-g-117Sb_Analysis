#################### RiP ##########################################
## Funtions to fit Gaussian, Lorentzian and Voigt curves to data ##
###################################################################

## ------------------------------- ##
from __future__ import print_function 
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import numpy as np
from scipy.optimize import curve_fit
## ------------------------------- ##

## Defines Voigt fit for n peaks
def nVoigt(x, *params):
    """
    Function to model the sum of n Voigt peaks.
    
    Parameters:
    x : ndarray
        The x-axis values (independent variable).
    *params : tuple
        A flattened list of parameters for 5 Voigt peaks.
        For each peak:
        - ampG: Amplitude of the Gaussian component.
        - cenG: Center of the Gaussian component.
        - sigmaG: Standard deviation (width) of the Gaussian.
        - ampL: Amplitude of the Lorentzian component.
        - cenL: Center of the Lorentzian component.
        - widL: Width of the Lorentzian.
        
        Total number of parameters = 5 peaks × 6 parameters/peak = 30 parameters.
    
    Returns:
    ndarray
        The sum of 5 Voigt peaks evaluated at x.
    """
    n_params_per_peak = 6
    n_peaks = len(params) // n_params_per_peak
    if len(params) != n_peaks * n_params_per_peak:
        raise ValueError(f"Expected {n_peaks * n_params_per_peak} parameters, got {len(params)}.")

    result = np.zeros_like(x, dtype=np.float64)

    # Loop over each peak and sum their contributions
    for i in range(n_peaks):
        ampG, cenG, sigmaG, ampL, cenL, widL = params[i * n_params_per_peak:(i + 1) * n_params_per_peak]
        gaussian = ampG * (1 / (sigmaG * np.sqrt(2 * np.pi))) * np.exp(-((x - cenG) ** 2) / (2 * sigmaG ** 2))
        lorentzian = ampL * widL ** 2 / ((x - cenL) ** 2 + widL ** 2)
        result += gaussian + lorentzian

    return result

## Define the Gaussian function
def gaussian(x, amp, mean, sigma):
    return amp * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))

## Define N Gaussian peaks
def nGaussian(x, *params):
    """
    Function to model n Gaussian peaks.
    params: Flattened list of parameters [amp1, cen1, sigma1, amp2, cen2, sigma2, ..., ampN, cenN, sigmaN]
    """
    n_params_per_peak = 3  # Each Gaussian has 3 parameters: amplitude, center, and sigma
    n_peaks = len(params) // n_params_per_peak
    result = np.zeros_like(x, dtype=np.float64)
    for i in range(n_peaks):
        amp, cen, sigma = params[i * n_params_per_peak:(i + 1) * n_params_per_peak]
        gaussian = amp * np.exp(-((x - cen) ** 2) / (2 * sigma ** 2))
        result += gaussian
    return result


## Fits function "func" to experimental data x and y, within certain regions of interest 
def FitData(func, x, y, init, lab, roid, roiu):
    """
    Uses scipy curve_fit to perform fit of a fucntion "func" to experimental data x and y, given initial guesses "init", in the regions of interest limited by roid and roiu.
    Writes the peak centroid and standard deviation into an output file with a costume name given by the label "lab".
    Prints the results into the terminal.
    Plots both the data and the fit.

    INPUTS - func: fucntion to fit; x: x-data; y: y-data; init: initial guess for fitting; lab: label for plot; roid: region of interest down; roiu: region of interest up;
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

## Fits multiple functions "func" to experimental data x and y
def FitNGauss(func, x, y, init, lab):
    """
    Uses scipy curve_fit to perform fit of a fucntion "func" to experimental data x and y, given initial guesses "init", for N cases, being N = len(init).
    Prints the results into the terminal.
    Plots both the data and the fit.

    INPUTS - func: fucntion to fit; x: x-data; y: y-data; init: initial guess for fitting; lab: label for plot;
    OUTPUTS - 
    """
    # Fit the data
    popt, pcov = curve_fit(func, x, y, p0=init)

    # Extract fitted parameters
    fitted_params = popt
    n_params_per_peak = 3
    n_peaks = len(init) // n_params_per_peak
    means = []
    std_devs = []
    amplitudes = []
    for i in range(n_peaks):
        amp, cen, sigma = fitted_params[i * n_params_per_peak:(i + 1) * n_params_per_peak]
        amplitudes.append(amp)
        means.append(cen)
        std_devs.append(sigma)

    # Extract uncertainty for sigma from the covariance matrix
    sigma_uncertainty = np.sqrt(np.diag(pcov))[2]  # Third parameter is sigma

    # Display the results
    print("***********************************"+len(lab)*"*")
    print("* Multi peak gaussian fit results "+lab+"*")
    print("***********************************"+len(lab)*"*")
    for i, (amp, mean, std_dev) in enumerate(zip(amplitudes, means, std_devs), start=1):
        print(f"Peak {i}: Amplitude = {amp:.2f}, Mean = {mean:.2f}, Std Dev = {std_dev:.2f} ± {sigma_uncertainty:.2f}")
    print()

    # Plot the results
    fig, ax = plt.subplots()
    ax.plot(x, y, '*-', color='blue', label=str("Exp. "+lab))
    ax.plot(x, nGaussian(x, *popt), '--', color='red', label="Fit")
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Channel")
    ylabel("Yield")
    title(f"Fit for {n_peaks} Gaussian Peaks")
    show()

    return
## --------------------------------------------------------------------------------------- ##
## --------------------------------------------------------------------------------------- ##

#######################
## Accumulation fits ##
#######################

## Defines Accumulation function as N_decay(t_acqui) = N_Dirr(1-exp(-lamb t_acqui))
def Ndecay(time, *params):

    """
    Function that models the accumulation of radioactive decays depending on the acquisition time.

    INPUTS:
    time : ndarray
        The x-axis variable, time of acquisition.
    *params : tuple
        A flattened list of parameters for the function:
        - N_Dirr: total number of radioactive nuclei in the target after the irradiation and the transportation time.
        - lamb: the decay caracteristic time, depending on the radioactive decay.

    OUPUTS: adjusted Ndecay curve
    """    
    Ndirr, lamb = params[0:2]
    return Ndirr * (1 - np.exp(-lamb * time))

## Funtion to fit accumulation curve to experimental data
def FitNdecay(func, time, counts, init, lab, roid, roiu):

    """
    INPUTS:
        - func: fucntion to fit;
        - time: acquisition time, the x-axis variable;
        - counts: accumulation yield in counts, the y-axis variable;
        - init: initial gusses for the fit parameters;
        - lab: a label to use for plotting;
    OUTPUTS:
    """

    time = np.array(time)
    counts = np.array(counts)

    # Restrict data to the ROI
    mask = (time >= roid) & (time <= roiu)
    time_roi = time[mask]
    counts_roi = counts[mask]


    ## Fit the data
    popt, pcov = curve_fit(func, time_roi, counts_roi, p0=init[0:2])

    ## Calculate the half-life
    halfLife_minutes = np.log(2)/popt[1] ## minutes
    halfLife_hours = halfLife_minutes/60 ## hours

    lamb_uncertainty_minutes = np.sqrt(np.diag(pcov))[1] ## minutes^-1
    lamb_uncertainty_hours = lamb_uncertainty_minutes/60 ## hours^-1 

    halfLife_hours_uncertainty = np.log(2)*lamb_uncertainty_hours/(popt[1]**2)

    ## Print results
    print("*****************************"+len(lab)*"*")
    print("* Accumulation fit results "+lab+"*")
    print("*****************************"+len(lab)*"*")
    print(f"T_1/2 = ({halfLife_hours:.2f} ± {halfLife_hours_uncertainty:.2f}) h")

    ## Fited function
    fitted = Ndecay(time_roi, *popt)

    # Plot the results
    fig, ax = plt.subplots()
    ax.semilogy(time, counts, '+-', color="blue", label=f"Ka line: {lab}")
    ax.semilogy(time_roi, fitted, '--', color="red", label="Fit")
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Time (minutes)", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit")
    show()

    return