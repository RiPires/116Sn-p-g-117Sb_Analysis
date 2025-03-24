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

## Defines Accumulation function for the number of radioactive decays as N_decay(t_acqui) = N_Dirr(1-exp(-lamb t_acqui))
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

    tTrans = 29. # minutes

    return Ndirr * np.exp(-lamb * tTrans) * (1 - np.exp(-lamb * time))

## Defines Accumulation function for the area under a photo-peak as N_peak(t_acqui) = \eta \epsilon_D exp(-lambda t_trans) N_Dirr (1-exp(-lamb t_acqui))
def NpeakHPGe(time, *params, radType, energy_key):
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
    efficiency_params = {
    'Ebeam=3.2MeV': {'gamma': (0.8590, 0.1762), 'Ka': (0.6750, 0.1575), 'Kb': (0.1419, 0.02860)},
    'Ebeam=3.5MeV': {'gamma': (0.8590, 0.1761), 'Ka': (0.6750, 0.1574), 'Kb': (0.1419, 0.02848)},
    'Ebeam=3.9MeV': {'gamma': (0.8590, 0.1762), 'Ka': (0.6750, 0.1576), 'Kb': (0.1419, 0.02844)},
    'Ebeam=4.3MeV': {'gamma': (0.8590, 0.1760), 'Ka': (0.6750, 0.1575), 'Kb': (0.1419, 0.02853)},
    'Ebeam=4.7MeV': {'gamma': (0.8590, 0.1763), 'Ka': (0.6750, 0.1577), 'Kb': (0.1419, 0.02837)},
    'Ebeam=5.0MeV': {'gamma': (0.8590, 0.1762), 'Ka': (0.6750, 0.1575), 'Kb': (0.1419, 0.02842)}
    }

    ## Transportation time (in minutes) for each activation energy
    t_transMin_key ={'Ebeam=3.2MeV': 63,
                     'Ebeam=3.5MeV': 29,
                     'Ebeam=3.9MeV': 32,
                     'Ebeam=4.3MeV': 40,
                     'Ebeam=4.7MeV': 31,
                     'Ebeam=5.0MeV': 29}
    
    try:
        Ndirr = float(params[0])  # Force conversion to float
    except ValueError:
        raise TypeError(f"Expected a numeric value for Ndirr, but got {params[0]} (type: {type(params[0])})")

    time = np.asarray(time, dtype=np.float64)  # Ensure time is a NumPy array

    ## Get efficiency and emission probability for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        eta, epsilonD = efficiency_params[energy_key][radType]
        t_transMin = t_transMin_key[energy_key]
    except KeyError:
        raise ValueError(f"Invalid energy '{energy_key}' or radType '{radType}'. Check input values.")

    ## Constants
    halfLifeMin = 2.8 * 60  # Decay half-life (minutes)
    lambda_decay = np.log(2) / halfLifeMin  # Decay constant

    ## Compute accumulation
    return eta * epsilonD * np.exp(-lambda_decay * t_transMin) * Ndirr * (1 - np.exp(-lambda_decay * time))

## Defines Accumulation function for the area under a photo-peak as N_peak(t_acqui) = \eta \epsilon_D exp(-lambda t_trans) N_Dirr (1-exp(-lamb t_acqui))
def NpeakSDD(time, *params, radType, energy_key):
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
    efficiency_params = {
    'Ebeam=3.2MeV': {'Ka': (0.6750, 3.842e-3), 'Kb': (0.1507, 4.733e-4)},
    'Ebeam=3.5MeV': {'Ka': (0.6750, 3.851e-3), 'Kb': (0.1507, 4.658e-4)},
    'Ebeam=3.9MeV': {'Ka': (0.6750, 3.844e-3), 'Kb': (0.1507, 4.553e-4)},
    'Ebeam=4.3MeV': {'Ka': (0.6750, 3.850e-3), 'Kb': (0.1507, 4.658e-4)},
    'Ebeam=4.7MeV': {'Ka': (0.6750, 3.846e-3), 'Kb': (0.1507, 4.642e-4)},
    'Ebeam=5.0MeV': {'Ka': (0.6750, 3.820e-3), 'Kb': (0.1507, 4.577e-4)}
    }

    ## Transportation time (in minutes) for each activation energy
    t_transMin_key ={'Ebeam=3.2MeV': 28,
                     'Ebeam=3.5MeV': 29,
                     'Ebeam=3.9MeV': 32,
                     'Ebeam=4.3MeV': 40,
                     'Ebeam=4.7MeV': 31,
                     'Ebeam=5.0MeV': 29}
    
    ## Get initial parameters to be fitted
    try:
        Ndirr, bgRate = float(params[0]),float(params[1])  # Force conversion to float
    except ValueError:
        raise TypeError(f"Expected a numeric value for Ndirr, bgRate but got {params[0]} (type: {type(params[0])}), and {params[1]} (type: {type(params[1])})")


    ## Ensure time is a NumPy array
    time = np.asarray(time, dtype=np.float64)  

    ## Get efficiency and emission probability for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        eta, epsilonD = efficiency_params[energy_key][radType]
        t_transMin = t_transMin_key[energy_key]
    except KeyError:
        raise ValueError(f"Invalid energy '{energy_key}' or radType '{radType}'. Check input values.")

    ## Constants
    halfLifeMin = 2.8 * 60  # Decay half-life (minutes)
    lambda_decay = np.log(2) / halfLifeMin  # Decay constant

    ## Compute accumulation
    return bgRate*time + eta * epsilonD * np.exp(-lambda_decay * t_transMin) * Ndirr * (1 - np.exp(-lambda_decay * time))

## Funtion to fit accumulation curve of number of decays to experimental data
## extracting decay half-life (T_1/2) and total nr. of radioactive nuclei 
## at the end of the activation (N_Dirr), for the HPGe detector
def FitNdecayHPGe(func, time, countsGamma, counts511, countsKa, countsKb, init, lab):
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
    countsGamma = np.array(countsGamma)
    counts511 = np.array(counts511)
    countsKa = np.array(countsKa)
    countsKb = np.array(countsKb)

    ## Fit the data
    poptGamma, pcovGamma = curve_fit(func, time, countsGamma, p0=init[0][0:3])
    popt511, pcov511 = curve_fit(func, time, counts511, p0=init[1][0:3])
    poptKa, pcovKa = curve_fit(func, time, countsKa, p0=init[2][0:3])
    poptKb, pcovKb = curve_fit(func, time, countsKb, p0=init[3][0:3])

    ## Calculate the half-life
    # Gamma line
    halfLifeGamma_minutes = np.log(2)/poptGamma[1] ## minutes
    halfLifeGamma_hours = halfLifeGamma_minutes/60 ## hours
    # 511 keV line
    halfLife511_minutes = np.log(2)/popt511[1] # minutes
    halfLife511_hours = halfLife511_minutes/60 # hours
    # Ka line
    halfLifeKa_minutes = np.log(2)/poptKa[1] ## minutes
    halfLifeKa_hours = halfLifeKa_minutes/60 ## hours
    # Kb line
    halfLifeKb_minutes = np.log(2)/poptKb[1] ## minutes
    halfLifeKb_hours = halfLifeKb_minutes/60 ## hours

    ## Calculate lambda uncertainty
    # Gamma line
    lambGamma_uncertainty_minutes = np.sqrt(np.diag(pcovGamma))[1] ## minutes^-1
    lambGamma_uncertainty_hours = lambGamma_uncertainty_minutes/60 ## hours^-1 
    # 511 keV line
    lamb511_uncertainty_minutes = np.sqrt(np.diag(pcov511))[1] ## minutes^-1
    lamb511_uncertainty_hours = lamb511_uncertainty_minutes/60 ## hours^-1 
    # Ka line
    lambKa_uncertainty_minutes = np.sqrt(np.diag(pcovKa))[1] ## minutes^-1
    lambKa_uncertainty_hours = lambKa_uncertainty_minutes/60 ## hours^-1 
    # Kb line
    lambKb_uncertainty_minutes = np.sqrt(np.diag(pcovKb))[1] ## minutes^-1
    lambKb_uncertainty_hours = lambKb_uncertainty_minutes/60 ## hours^-1 

    ## Calculate half-life uncertainty
    halfLifeGamma_hours_uncertainty = np.log(2)*lambGamma_uncertainty_hours/(poptGamma[1]**2)
    halfLife511_hours_uncertainty = np.log(2)*lamb511_uncertainty_hours/(popt511[1]**2)
    halfLifeKa_hours_uncertainty = np.log(2)*lambKa_uncertainty_hours/(poptKa[1]**2)
    halfLifeKb_hours_uncertainty = np.log(2)*lambKb_uncertainty_hours/(poptKb[1]**2)

    ## Get fitted Ndirr and tTrans
    NdirrGamma = poptGamma[0]
    Ndirr511 = popt511[0]
    NdirrKa = poptKa[0]
    NdirrKb= poptKb[0]

    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Gamma line: \t T_1/2 = ({halfLifeGamma_hours:.2f} ± {halfLifeGamma_hours_uncertainty:.2f}) h, \t Ndirr = {NdirrGamma:.2e}")
    print(f"511 keV line: \t T_1/2 = ({halfLife511_hours:.2f} ± {halfLife511_hours_uncertainty:.2f}) h, \t Ndirr = {Ndirr511:.2e}")
    print(f"Ka line: \t T_1/2 = ({halfLifeKa_hours:.2f} ± {halfLifeKa_hours_uncertainty:.2f}) h, \t Ndirr = {NdirrKa:.2e}")
    print(f"Kb line: \t T_1/2 = ({halfLifeKb_hours:.2f} ± {halfLifeKb_hours_uncertainty:.2f}) h, \t Ndirr = {NdirrKb:.2e}")
    print()

    ## Fited function
    fittedGamma = Ndecay(time, *poptGamma)
    fitted511 = Ndecay(time, *popt511)
    fittedKa = Ndecay(time, *poptKa)
    fittedKb = Ndecay(time, *poptKb)

    # Plot the results
    fig, ax = plt.subplots()
    ax.semilogy(time, countsGamma, '*', color="xkcd:sky blue", label=f"Gamma")
    ax.semilogy(time, fittedGamma, '-', color="xkcd:blue", label="Fit - Gamma")
    ax.semilogy(time, counts511, 'D', color="xkcd:maize", label=f"511 keV")
    ax.semilogy(time, fitted511, '-', color="xkcd:orange yellow", label=f"Fit - 511 keV")
    ax.semilogy(time, countsKa, '^', color="xkcd:turquoise", label=f"Ka")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - Ka")
    ax.semilogy(time, countsKb, 'v', color="xkcd:salmon", label=f"Kb")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - Kb")
    legend = ax.legend(loc="best",ncol=4,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Time (minutes)", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit Ndecay: "+lab, fontsize=24)
    show()

    return

## Funtion to fit accumulation curve of number of decays to experimental data
## extracting decay half-life (T_1/2) and total nr. of radioactive nuclei 
## at the end of the activation (N_Dirr), for the SDD detector
def FitNdecaySDD(func, time, countsKa, countsKb, init, lab):
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
    countsKa = np.array(countsKa)
    countsKb = np.array(countsKb)

    ## Fit the data
    poptKa, pcovKa = curve_fit(func, time, countsKa, p0=init[0][0:2])
    poptKb, pcovKb = curve_fit(func, time, countsKb, p0=init[1][0:2])

    ## Calculate the half-life
    halfLifeKa_minutes = np.log(2)/poptKa[1] ## minutes
    halfLifeKa_hours = halfLifeKa_minutes/60 ## hours
    halfLifeKb_minutes = np.log(2)/poptKb[1] ## minutes
    halfLifeKb_hours = halfLifeKb_minutes/60 ## hours

    lambKa_uncertainty_minutes = np.sqrt(np.diag(pcovKa))[1] ## minutes^-1
    lambKa_uncertainty_hours = lambKa_uncertainty_minutes/60 ## hours^-1 
    lambKb_uncertainty_minutes = np.sqrt(np.diag(pcovKb))[1] ## minutes^-1
    lambKb_uncertainty_hours = lambKb_uncertainty_minutes/60 ## hours^-1 

    halfLifeKa_hours_uncertainty = np.log(2)*lambKa_uncertainty_hours/(poptKa[1]**2)
    halfLifeKb_hours_uncertainty = np.log(2)*lambKb_uncertainty_hours/(poptKb[1]**2)

    ## Get fitted Ndirr and tTrans
    NdirrKa = poptKa[0]
    NdirrKb= poptKb[0]

    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Ka line:    T_1/2 = ({halfLifeKa_hours:.2f} ± {halfLifeKa_hours_uncertainty:.2f}) h, \t Ndirr = {NdirrKa:.2e}")
    print(f"Kb line:    T_1/2 = ({halfLifeKb_hours:.2f} ± {halfLifeKb_hours_uncertainty:.2f}) h, \t Ndirr = {NdirrKb:.2e}")
    print()

    ## Fited function
    fittedKa = Ndecay(time, *poptKa)
    fittedKb = Ndecay(time, *poptKb)

    # Plot the results
    fig, ax = plt.subplots()
    ax.semilogy(time, countsKa, '^', color="xkcd:turquoise", label=f"Ka")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - Ka")
    ax.semilogy(time, countsKb, 'v', color="xkcd:salmon", label=f"Kb")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - Kb")
    legend = ax.legend(loc="best",ncol=3,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Time (minutes)", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit Ndecay: "+lab, fontsize=24)
    show()

    return

## ************************************************************************************ ##
## Funtion to fit accumulation curve of area under a photo-peak to experimental data    ##
## extracting decay half-life (T_1/2), total nr. of radioactive nuclei at the end of    ##
## the activation (N_Dirr), decay branching ratio (eta), detector efficiency (epsilonD) ##
## and transportation time (t_trans), for the HPGe detector                             ##
## ************************************************************************************ ##
def FitNpeakHPGe(func, time, countsGamma, errGamma, countsKa, errKa, countsKb, errKb, init, lab, energy_key):
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
    poptGamma, pcovGamma = curve_fit(lambda t, *p: NpeakHPGe(t, *p, radType='gamma', energy_key=energy_key), 
                                     time, countsGamma, p0=init[0][0:2])
    
    poptKa, pcovKa = curve_fit(lambda t, *p: NpeakHPGe(t, *p, radType='Ka', energy_key=energy_key), 
                               time, countsKa, p0=init[1][0:2])
    
    poptKb, pcovKb = curve_fit(lambda t, *p: NpeakHPGe(t, *p, radType='Kb', energy_key=energy_key), 
                               time, countsKb, p0=init[2][0:2])

    """     ## Calculate the half-life
    # Gamma line
    halfLifeGamma_minutes = np.log(2)/poptGamma[1] ## minutes
    halfLifeGamma_hours = halfLifeGamma_minutes/60 ## hours
    # Ka line
    halfLifeKa_minutes = np.log(2)/poptKa[1] ## minutes
    halfLifeKa_hours = halfLifeKa_minutes/60 ## hours
    # Kb line
    halfLifeKb_minutes = np.log(2)/poptKb[1] ## minutes
    halfLifeKb_hours = halfLifeKb_minutes/60 ## hours

    ## Calculate lambda uncertainty
    # Gamma line
    lambGamma_uncertainty_minutes = np.sqrt(np.diag(pcovGamma))[1] ## minutes^-1
    lambGamma_uncertainty_hours = lambGamma_uncertainty_minutes/60 ## hours^-1 
    # Ka line
    lambKa_uncertainty_minutes = np.sqrt(np.diag(pcovKa))[1] ## minutes^-1
    lambKa_uncertainty_hours = lambKa_uncertainty_minutes/60 ## hours^-1 
    # Kb line
    lambKb_uncertainty_minutes = np.sqrt(np.diag(pcovKb))[1] ## minutes^-1
    lambKb_uncertainty_hours = lambKb_uncertainty_minutes/60 ## hours^-1 

    ## Calculate half-life uncertainty in hours
    halfLifeGamma_hours_uncertainty = np.log(2)*lambGamma_uncertainty_hours/(poptGamma[1]**2)   # Gamma line
    halfLifeKa_hours_uncertainty = np.log(2)*lambKa_uncertainty_hours/(poptKa[1]**2)            # Ka line
    halfLifeKb_hours_uncertainty = np.log(2)*lambKb_uncertainty_hours/(poptKb[1]**2)            # Kb line
    """
    
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
    fittedGamma = NpeakHPGe(time, *poptGamma, radType='gamma', energy_key=energy_key)
    fittedKa = NpeakHPGe(time, *poptKa, radType='Ka', energy_key=energy_key)
    fittedKb = NpeakHPGe(time, *poptKb, radType='Kb', energy_key=energy_key)

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
def FitNpeakSDD(func, time, countsKa, errKa, countsKb, errKb, init, lab, energy_key):
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
    poptKa, pcovKa = curve_fit(lambda t, *p: NpeakSDD(t, *p, radType='Ka', energy_key=energy_key), 
                               time, countsKa, p0=init[0][0:3])
    
    poptKb, pcovKb = curve_fit(lambda t, *p: NpeakSDD(t, *p, radType='Kb', energy_key=energy_key), 
                               time, countsKb, p0=init[1][0:3])
    
    ## Get fit parameters
    # Ka line
    NdirrKa, NdirrKa_err = poptKa[0], np.sqrt(np.diag(pcovKa))[0]
    bgRateKa, bgRateKa_err = poptKa[1], np.sqrt(np.diag(pcovKa))[1]
    # Kb line
    NdirrKb, NdirrKb_err = poptKb[0], np.sqrt(np.diag(pcovKb))[0]
    bgRateKb, bgRateKb_err = poptKb[1], np.sqrt(np.diag(pcovKb))[1]

    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e}")
    print(f"\t \t bgRate = ({bgRateKa:.3f}+-{bgRateKa_err:.3f})/30 min")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e}")
    print(f"\t \t bgRate = ({bgRateKb:.3f}+-{bgRateKb_err:.3f})/30 min")
    print(f"Ka/Kb ratio = \t {(NdirrKa/NdirrKb):.3e}")
    print()

    ## Fit function for plotting
    fittedKa = NpeakSDD(time, *poptKa, radType='Ka', energy_key=energy_key)
    fittedKb = NpeakSDD(time, *poptKb, radType='Kb', energy_key=energy_key)

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