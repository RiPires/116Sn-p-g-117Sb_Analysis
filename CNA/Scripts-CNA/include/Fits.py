############################ RiP ##############################
## Funtions to fit Gaussian, and accumulation curves to data ##
###############################################################

## ------------------------------- ##
from __future__ import print_function 
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import numpy as np
from scipy.optimize import curve_fit
## ------------------------------- ##

## Define the Gaussian function
def gaussian(x, amp, mean, sigma, backGround):
    return amp * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2)) + backGround*x

## Define N Gaussian peaks
def nGaussian(x, *params):
    """
    Function to model n Gaussian peaks.
    params: Flattened list of parameters [amp1, cen1, sigma1, amp2, cen2, sigma2, ..., ampN, cenN, sigmaN]
    """
    ## Initialize array to store resuts
    n_params_per_peak = 3  # Each Gaussian has 3 parameters: amplitude, center, and sigma
    n_peaks = len(params) // n_params_per_peak
    result = np.zeros_like(x, dtype=np.float64)
    
    ## Loop over each peak
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
    
    x    = np.array(x)
    y    = np.array(y)
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
            p0 = init[i]
            # Fit the data within the ROI
            popt, pcov = curve_fit(func, x_roi, y_roi, p0=p0)
            fitted_params.append(popt)
            # Add current fit to the combined result
            all_fits += gaussian(x, *popt)
            # Extract uncertainty for sigma from the covariance matrix
            sigma_uncertainty = np.sqrt(np.diag(pcov))[2]  # Third parameter is sigma
            # Write results to file
            amp, mean, sigma, backGround = popt
            outFile.write(f"{mean:.2f}\t{sigma:.2f}\t{sigma_uncertainty:.2f}\n")
    outFile.close()

    # Print results
    print("*************************************"+len(lab)*"*")
    print("* Single peak gaussian fit results "+lab+"*")
    print("*************************************"+len(lab)*"*")
    for i, param in enumerate(fitted_params, start=1):
        print(f"Peak {i}: Amplitude = {param[0]:.2f}, Mean = {param[1]:.2f}, Sigma = {param[2]:.2f} ± {sigma_uncertainty:.2f}, BackGround = {param[3]:.2f}")
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

## ***************** ##
## Accumulation fits ##
## ***************** ##

## ************************************************************************************ ##
## Defines Accumulation function for the area under a photo-peak as                     ##   
## N_peak(t_acqui) = bgRate*t_acqui + N0 * (1-exp(-lamb t_acqui))                       ##
## ************************************************************************************ ##
def Npeak(time, *params):
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

    ## Set parameters to fit
    try:
        N0, bgRate = float(params[0]), float(params[1])  # Force conversion to float
    except ValueError:
        raise TypeError(f"Expected a numeric value for Ndirr, but got {params[0]} (type: {type(params[0])})")

    ## Set time array
    time = np.asarray(time, dtype=np.float64)  # Ensure time is a NumPy array

    ## Constants
    halfLifeMin = 2.8 * 60  # Decay half-life (minutes)
    lambda_decay = np.log(2) / halfLifeMin  # Decay constant

    ## Compute accumulation
    return bgRate*time +  N0 * (1 - np.exp(-lambda_decay * time))

## ************************************************************************************ ##
## Defines Accumulation function for the area under a photo-peak as                     ##   
## N_peak(t_acqui) = bgRate*t_acqui + N0 * (1-exp(-lamb t_acqui))                       ##
## ************************************************************************************ ##
def NpeakHalfLife(time, t_trans, *params):
    """
    Function that models the accumulation of radioactive decays over the acquisition time,
    keeping N0, and decay Half-Life as free parameters.

    INPUTS:
    time: ndarray
        The x-axis variable, time of acquisition.
    *params: tuple
        A flattened list of parameters for the function:
        - N0 (int):     saturation value of the accumulation curves, that relates 
                        to the total number of radioactive nuclei in the target 
                        after the irradiation and the transportation time.
        - lamb (float): the decay caracteristic time, depending on the radioactive decay.

    OUPUTS: adjusted Npeak curve
    """    
    ## Set parameters to fit
    N0, lambda_decay = float(params[0]), float(params[1])

    ## Set acquisition time, ensuring it is a NumPy array
    time = np.asarray(time, dtype=np.float64)

    ## Compute accumulation
    return N0 * np.exp(-lambda_decay*t_trans) * (1 - np.exp(-lambda_decay * time))

## ***************************************************************************************************** ##
## Funtion to fit accumulation curve to experimental data, extracting total nr. of radioactive nuclei at ##
## the end of the irradiation (N_Dirr) for the HPGe detector                                             ##
## ***************************************************************************************************** ##
def FitNpeakHPGe(func, time, countsGamma, errGamma, countsKa, errKa, countsKb, errKb, counts511, err511, counts861, err861, counts1004, err1004, init, efficiency, t_trans, lab, energy_key, radType):
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
    time        = np.array(time)
    countsGamma = np.array(countsGamma)
    countsKa    = np.array(countsKa)
    countsKb    = np.array(countsKb)
    counts511   = np.array(counts511)
    counts861   = np.array(counts861)
    counts1004  = np.array(counts1004)

    ## Fit the data, passing radType explicitly
    # Gamma line
    poptGamma, pcovGamma    = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, countsGamma, p0=init[radType[0]][0:2], sigma=errGamma[1:], absolute_sigma=True)
    # Ka line
    poptKa, pcovKa          = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, countsKa, p0=init[radType[1]][0:2], sigma=errKa[1:], absolute_sigma=True)
    # Kb line
    poptKb, pcovKb          = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, countsKb, p0=init[radType[2]][0:2], sigma=errKb[1:], absolute_sigma=True)
    # 511 keV line
    popt511, pcov511        = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, counts511, p0=init[radType[3]][0:2], sigma=err511[1:], absolute_sigma=True)
    # 861 keV line
    popt861, pcov861        = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, counts861, p0=init[radType[4]][0:2], sigma=err861[1:], absolute_sigma=True)
    # 1004 keV line
    popt1004, pcov1004      = curve_fit(lambda t, *p: Npeak(t, *p), 
                                        time, counts1004, p0=init[radType[5]][0:2], sigma=err1004[1:], absolute_sigma=True)
    
    ## Get fit parameters and std_dev = sqrt(variance) = sqrt(diag(cov))
    # Gamma line
    N0Gamma, N0Gamma_err            = poptGamma[0], np.sqrt(np.diag(pcovGamma))[0]
    bgRateGamma, bgRateGamma_err    = poptGamma[1], np.sqrt(np.diag(pcovGamma))[1]
    # Ka line 
    N0Ka, N0Ka_err                  = poptKa[0],    np.sqrt(np.diag(pcovKa))[0]
    bgRateKa, bgRateKa_err          = poptKa[1],    np.sqrt(np.diag(pcovKa))[1]
    # Kb line   
    N0Kb, N0Kb_err                  = poptKb[0],    np.sqrt(np.diag(pcovKb))[0]  
    bgRateKb, bgRateKb_err          = poptKb[1],    np.sqrt(np.diag(pcovKb))[1]
    # 511 keV line   
    N0511, N0511_err                = popt511[0],   np.sqrt(np.diag(pcov511))[0]  
    bgRate511, bgRate511_err        = popt511[1],   np.sqrt(np.diag(pcov511))[1]
    # 861 keV line   
    N0861, N0861_err                = popt861[0],   np.sqrt(np.diag(pcov861))[0]  
    bgRate861, bgRate861_err        = popt861[1],   np.sqrt(np.diag(pcov861))[1]
    # 1004 keV line   
    N01004, N01004_err              = popt1004[0],   np.sqrt(np.diag(pcov1004))[0]  
    bgRate1004, bgRate1004_err      = popt1004[1],   np.sqrt(np.diag(pcov1004))[1]

    ## Constants
    halfLifeMin         = 2.8 * 60  # Decay half-life (minutes)
    halfLife_min_err    = 0.01*60 # minutes
    lambda_decay        = np.log(2) / halfLifeMin  # Decay constant
    lambda_decay_err    = np.log(2) * halfLife_min_err / halfLifeMin**2  # in min^-1
    t_trans_err         = 1. # minute

    ## Calculate N_Dirr and error propagation
    ## Gamma line
    NdirrGamma      = N0Gamma/(efficiency[0][0] * np.exp(-lambda_decay*t_trans))
    NdirrGamma_err  = np.sqrt((np.exp(lambda_decay*t_trans)*N0Gamma_err/efficiency[0][0])**2 + 
                            (N0Gamma*np.exp(lambda_decay*t_trans)*efficiency[0][1]/efficiency[0][0]**2)**2 + 
                            (t_trans*N0Gamma*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[0][0])**2 + 
                            (lambda_decay*N0Gamma*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[0][0])**2)
    ## Ka line
    NdirrKa         = N0Ka/(efficiency[1][0] * np.exp(-lambda_decay*t_trans))
    NdirrKa_err     = np.sqrt((np.exp(lambda_decay*t_trans)*N0Ka_err/efficiency[1][0])**2 + 
                            (N0Ka*np.exp(lambda_decay*t_trans)*efficiency[1][1]/efficiency[1][0]**2)**2 + 
                            (t_trans*N0Ka*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[1][0])**2 + 
                            (lambda_decay*N0Ka*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[1][0])**2)
    ## Kb line
    NdirrKb         = N0Kb/(efficiency[2][0] * np.exp(-lambda_decay*t_trans))
    NdirrKb_err     = np.sqrt((np.exp(lambda_decay*t_trans)*N0Kb_err/efficiency[2][0])**2 + 
                            (N0Kb*np.exp(lambda_decay*t_trans)*efficiency[2][1]/efficiency[2][0]**2)**2 + 
                            (t_trans*N0Kb*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[2][0])**2 + 
                            (lambda_decay*N0Kb*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[2][0])**2)
    ## 511 keV line
    Ndirr511        = N0511/(efficiency[3][0] * np.exp(-lambda_decay*t_trans))
    Ndirr511_err    = np.sqrt((np.exp(lambda_decay*t_trans)*N0511_err/efficiency[3][0])**2 + 
                            (N0511*np.exp(lambda_decay*t_trans)*efficiency[3][1]/efficiency[3][0]**2)**2 + 
                            (t_trans*N0511*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[3][0])**2 + 
                            (lambda_decay*N0511*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[3][0])**2)
    ## 861 keV line
    Ndirr861        = N0861/(efficiency[4][0] * np.exp(-lambda_decay*t_trans))
    Ndirr861_err    = np.sqrt((np.exp(lambda_decay*t_trans)*N0861_err/efficiency[4][0])**2 + 
                            (N0861*np.exp(lambda_decay*t_trans)*efficiency[4][1]/efficiency[4][0]**2)**2 + 
                            (t_trans*N0861*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[4][0])**2 + 
                            (lambda_decay*N0861*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[4][0])**2)
    ## 1004 keV line
    Ndirr1004       = N01004/(efficiency[5][0] * np.exp(-lambda_decay*t_trans))
    Ndirr1004_err   = np.sqrt((np.exp(lambda_decay*t_trans)*N01004_err/efficiency[5][0])**2 + 
                            (N01004*np.exp(lambda_decay*t_trans)*efficiency[5][1]/efficiency[5][0]**2)**2 + 
                            (t_trans*N01004*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[5][0])**2 + 
                            (lambda_decay*N01004*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[5][0])**2)
    
    ## Print results
    """     print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Gamma line: \t Ndirr = {NdirrGamma:.3e} +- {NdirrGamma_err:.0e} | bgRate = ({bgRateGamma:.2f} +- {bgRateGamma_err:.2f}) counts/min")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e} | bgRate = ({bgRateKa:.2f} +- {bgRateKa_err:.2f}) counts/min")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e} | bgRate = ({bgRateKb:.2f} +- {bgRateKb_err:.2f}) counts/min")
    print(f"511 keV line: \t Ndirr = {Ndirr511:.3e} +- {Ndirr511_err:.0e} | bgRate = ({bgRate511:.2f} +- {bgRate511_err:.2f}) counts/min")
    print(f"861 keV line: \t Ndirr = {Ndirr861:.3e} +- {Ndirr861_err:.0e} | bgRate = ({bgRate861:.2f} +- {bgRate861_err:.2f}) counts/min")
    print(f"1004 keV line: \t Ndirr = {Ndirr1004:.3e} +- {Ndirr1004_err:.0e} | bgRate = ({bgRate1004:.2f} +- {bgRate1004_err:.2f}) counts/min")
    print(f"gamma/Ka = {(NdirrGamma/NdirrKa):.2f} | gamma/Kb = {(NdirrGamma/NdirrKb):.2f} | Ka/Kb = {(NdirrKa/NdirrKb):.2f}")
    print()
    """
    ## Create dictionary for results
    N_D_irr_SDD = {
        energy_key: {
            "Gamma": NdirrGamma,
            "Ka": NdirrKa,
            "Kb": NdirrKb,
            "511 keV": Ndirr511,
            "861 keV": Ndirr861,
            "1004 keV": Ndirr1004
        }
    }

    ## Print dictionary
    for key, value in N_D_irr_SDD.items():
        print(f'    "{key}": {{"gamma": {value["Gamma"]:.3e}, "Ka": {value["Ka"]:.3e}, "Kb": {value["Kb"]:.3e},"511 keV": {value["511 keV"]:.3e}, "861 keV": {value["861 keV"]:.3e}, "1004 keV": {value["1004 keV"]:.3e}}},')


    ## Fited function for plotting
    fittedGamma = Npeak(time, *poptGamma)
    fittedKa    = Npeak(time, *poptKa)
    fittedKb    = Npeak(time, *poptKb)
    fitted511   = Npeak(time, *popt511)
    fitted861   = Npeak(time, *popt861)
    fitted1004  = Npeak(time, *popt1004)

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    #ax.errorbar(time, counts1004, yerr=err1004[1:], fmt='+', color='xkcd:red orange', label="1004 keV")
    #ax.semilogy(time, fitted1004, '-', color='xkcd:coral', label="Fit - 1004 keV")
    #ax.errorbar(time, counts861, yerr=err861[1:], fmt='+', color='xkcd:orange', label="861 keV")
    #ax.semilogy(time, fitted861, '-', color='xkcd:tan', label="Fit - 861 keV")
    #ax.errorbar(time, counts511, yerr=err511[1:], fmt='+', color='xkcd:purple', label="511 keV")
    #ax.semilogy(time, fitted511, '-', color='xkcd:lavender', label="Fit -511 keV")
    ax.errorbar(time, countsGamma, yerr=errGamma[1:], fmt='*', color="xkcd:sky blue", label=f"Gamma")
    ax.semilogy(time, fittedGamma, '-', color="xkcd:blue", label="Fit - Gamma")
    ax.errorbar(time, countsKa, yerr=errKa[1:], fmt='^', color="xkcd:turquoise", label=f"Ka")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - Ka")
    ax.errorbar(time, countsKb, yerr=errKb[1:],fmt='v', color="xkcd:salmon", label=f"Kb")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - Kb")
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Acquisition Time [minutes]", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit: "+lab, fontsize=24)
    show()

    return

## ***************************************************************************************************** ##
## Funtion to fit accumulation curve to HPGe detector experimental data, extracting total nr. of         ##
## radioactive nuclei at the end of the irradiation (N_Dirr) and decay Half-Life, for the  data          ##
## ***************************************************************************************************** ##
def FitNpeakHalfLifeHPGe(func, time, countsGamma, errGamma, countsKa, errKa, countsKb, errKb, counts511, err511, counts861, err861, counts1004, err1004, init, efficiency, t_trans, lab, energy_key, radType):
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
    time        = np.array(time)
    countsGamma = np.array(countsGamma)
    countsKa    = np.array(countsKa)
    countsKb    = np.array(countsKb)
    counts511   = np.array(counts511)
    counts861   = np.array(counts861)
    counts1004  = np.array(counts1004)

    ## Fit the data, passing radType explicitly
    # Gamma line
    poptGamma, pcovGamma    = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, countsGamma, p0=init[radType[0]][0:2], sigma=errGamma[1:], absolute_sigma=True)
    # Ka line
    poptKa, pcovKa          = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, countsKa, p0=init[radType[1]][0:2], sigma=errKa[1:], absolute_sigma=True)
    # Kb line
    poptKb, pcovKb          = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, countsKb, p0=init[radType[2]][0:2], sigma=errKb[1:], absolute_sigma=True)
    # 511 keV line
    popt511, pcov511        = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, counts511, p0=init[radType[3]][0:2], sigma=err511[1:], absolute_sigma=True)
    # 861 keV line
    popt861, pcov861        = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, counts861, p0=init[radType[4]][0:2], sigma=err861[1:], absolute_sigma=True)
    # 1004 keV line
    popt1004, pcov1004      = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, counts1004, p0=init[radType[5]][0:2], sigma=err1004[1:], absolute_sigma=True)
    
    ## Get fit parameters and std_dev = sqrt(variance) = sqrt(diag(cov))
    # Gamma line
    N0Gamma, N0Gamma_err            = poptGamma[0], np.sqrt(np.diag(pcovGamma))[0]
    lambdaGamma, lambdaGamma_err    = poptGamma[1], np.sqrt(np.diag(pcovGamma))[1]
    # Ka line 
    N0Ka, N0Ka_err                  = poptKa[0],    np.sqrt(np.diag(pcovKa))[0]
    lambdaKa, lambdaKa_err          = poptKa[1],    np.sqrt(np.diag(pcovKa))[1]
    # Kb line   
    N0Kb, N0Kb_err                  = poptKb[0],    np.sqrt(np.diag(pcovKb))[0]  
    lambdaKb, lambdaKb_err          = poptKb[1],    np.sqrt(np.diag(pcovKb))[1]
    # 511 keV line   
    N0511, N0511_err                = popt511[0],   np.sqrt(np.diag(pcov511))[0]  
    lambda511, lambda511_err        = popt511[1],   np.sqrt(np.diag(pcov511))[1]
    # 861 keV line   
    N0861, N0861_err                = popt861[0],   np.sqrt(np.diag(pcov861))[0]  
    lambda861, lambda861_err        = popt861[1],   np.sqrt(np.diag(pcov861))[1]
    # 1004 keV line   
    N01004, N01004_err              = popt1004[0],  np.sqrt(np.diag(pcov1004))[0]  
    lambda1004, lambda1004_err      = popt1004[1],  np.sqrt(np.diag(pcov1004))[1]

    ## Constants
    t_trans_err         = 1. # minute

    ## Calculate Half-Lifes from fitted lambdas
    ## Gamma line
    hLifeMinGamma       = np.log(2)/lambdaGamma
    hLifeMinGamma_err   = hLifeMinGamma*lambdaGamma_err/lambdaGamma
    ## Ka line
    hLifeMinKa          = np.log(2)/lambdaKa
    hLifeMinKa_err      = hLifeMinKa*lambdaKa_err/lambdaKa
    ## Kb line
    hLifeMinKb          = np.log(2)/lambdaKb
    hLifeMinKb_err      = hLifeMinKb*lambdaKb_err/lambdaKb
    ## 511 keV line
    hLifeMin511         = np.log(2)/lambda511
    hLifeMin511_err     = hLifeMin511*lambda511_err/lambda511
    ## 861 keV line
    hLifeMin861         = np.log(2)/lambda861
    hLifeMin861_err     = hLifeMin861*lambda861_err/lambda861
    ## 1004 keV line
    hLifeMin1004        = np.log(2)/lambda1004
    hLifeMin1004_err    = hLifeMin1004*lambda1004_err/lambda1004
    

    ## Calculate N_Dirr and error propagation
    ## Gamma line
    NdirrGamma      = N0Gamma/efficiency[0][0]
    NdirrGamma_err  = np.sqrt((np.exp(lambdaGamma*t_trans)*N0Gamma_err/efficiency[0][0])**2 + 
                            (N0Gamma*np.exp(lambdaGamma*t_trans)*efficiency[0][1]/efficiency[0][0]**2)**2 + 
                            (t_trans*N0Gamma*np.exp(lambdaGamma*t_trans)*lambdaGamma_err/efficiency[0][0])**2 + 
                            (lambdaGamma*N0Gamma*np.exp(lambdaGamma*t_trans)*t_trans_err/efficiency[0][0])**2)
    ## Ka line
    NdirrKa         = N0Ka/efficiency[1][0] 
    NdirrKa_err     = np.sqrt((np.exp(lambdaKa*t_trans)*N0Ka_err/efficiency[1][0])**2 + 
                            (N0Ka*np.exp(lambdaKa*t_trans)*efficiency[1][1]/efficiency[1][0]**2)**2 + 
                            (t_trans*N0Ka*np.exp(lambdaKa*t_trans)*lambdaKa_err/efficiency[1][0])**2 + 
                            (lambdaKa*N0Ka*np.exp(lambdaKa*t_trans)*t_trans_err/efficiency[1][0])**2)
    ## Kb line
    NdirrKb         = N0Kb/efficiency[2][0]
    NdirrKb_err     = np.sqrt((np.exp(lambdaKb*t_trans)*N0Kb_err/efficiency[2][0])**2 + 
                            (N0Kb*np.exp(lambdaKb*t_trans)*efficiency[2][1]/efficiency[2][0]**2)**2 + 
                            (t_trans*N0Kb*np.exp(lambdaKb*t_trans)*lambdaKb_err/efficiency[2][0])**2 + 
                            (lambdaKb*N0Kb*np.exp(lambdaKb*t_trans)*t_trans_err/efficiency[2][0])**2)
    ## 511 keV line
    Ndirr511        = N0511/efficiency[3][0]
    Ndirr511_err    = np.sqrt((np.exp(lambda511*t_trans)*N0511_err/efficiency[3][0])**2 + 
                            (N0511*np.exp(lambda511*t_trans)*efficiency[3][1]/efficiency[3][0]**2)**2 + 
                            (t_trans*N0511*np.exp(lambda511*t_trans)*lambda511_err/efficiency[3][0])**2 + 
                            (lambda511*N0511*np.exp(lambda511*t_trans)*t_trans_err/efficiency[3][0])**2)
    ## 861 keV line
    Ndirr861        = N0861/efficiency[4][0]
    Ndirr861_err    = np.sqrt((np.exp(lambda861*t_trans)*N0861_err/efficiency[4][0])**2 + 
                            (N0861*np.exp(lambda861*t_trans)*efficiency[4][1]/efficiency[4][0]**2)**2 + 
                            (t_trans*N0861*np.exp(lambda861*t_trans)*lambda861_err/efficiency[4][0])**2 + 
                            (lambda861*N0861*np.exp(lambda861*t_trans)*t_trans_err/efficiency[4][0])**2)
    ## 1004 keV line
    Ndirr1004       = N01004/efficiency[5][0]
    Ndirr1004_err   = np.sqrt((np.exp(lambda1004*t_trans)*N01004_err/efficiency[5][0])**2 + 
                            (N01004*np.exp(lambda1004*t_trans)*efficiency[5][1]/efficiency[5][0]**2)**2 + 
                            (t_trans*N01004*np.exp(lambda1004*t_trans)*lambda1004_err/efficiency[5][0])**2 + 
                            (lambda1004*N01004*np.exp(lambda1004*t_trans)*t_trans_err/efficiency[5][0])**2)
    
    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Gamma line: \t Ndirr = {NdirrGamma:.3e} +- {NdirrGamma_err:.0e} | Half-Life = ({(hLifeMinGamma/60):.2f} +- {(hLifeMinGamma_err/60):.2f}) hours")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e} | Half-Life = ({(hLifeMinKa/60):.2f} +- {(hLifeMinKa_err/60):.2f}) hours")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e} | Half-Life = ({(hLifeMinKb/60):.2f} +- {(hLifeMinKb_err/60):.2f}) hours")
    print(f"511 keV line: \t Ndirr = {Ndirr511:.3e} +- {Ndirr511_err:.0e} | Half-Life = ({(hLifeMin511/60):.2f} +- {(hLifeMin511_err/60):.2f}) hours")
    print(f"861 keV line: \t Ndirr = {Ndirr861:.3e} +- {Ndirr861_err:.0e} | Half-Life = ({(hLifeMin861/60):.2f} +- {(hLifeMin861_err/60):.2f}) hours")
    print(f"1004 keV line: \t Ndirr = {Ndirr1004:.3e} +- {Ndirr1004_err:.0e} | Half-Life = ({(hLifeMin1004/60):.2f} +- {(hLifeMin1004_err/60):.2f}) hours")
    print(f"gamma/Ka = {(NdirrGamma/NdirrKa):.2f} | gamma/Kb = {(NdirrGamma/NdirrKb):.2f} | Ka/Kb = {(NdirrKa/NdirrKb):.2f}")
    print()

    ## Fited function for plotting
    fittedGamma = NpeakHalfLife(time, t_trans, *poptGamma)
    fittedKa    = NpeakHalfLife(time, t_trans, *poptKa)
    fittedKb    = NpeakHalfLife(time, t_trans, *poptKb)
    fitted511   = NpeakHalfLife(time, t_trans, *popt511)
    fitted861   = NpeakHalfLife(time, t_trans, *popt861)
    fitted1004  = NpeakHalfLife(time, t_trans, *popt1004)

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.errorbar(time, counts1004, yerr=err1004[1:], fmt='+', color='xkcd:red orange', label="1004 keV")
    ax.semilogy(time, fitted1004, '-', color='xkcd:coral', label="Fit - 1004 keV")
    ax.errorbar(time, counts861, yerr=err861[1:], fmt='+', color='xkcd:orange', label="861 keV")
    ax.semilogy(time, fitted861, '-', color='xkcd:tan', label="Fit - 861 keV")
    ax.errorbar(time, counts511, yerr=err511[1:], fmt='+', color='xkcd:purple', label="511 keV")
    ax.semilogy(time, fitted511, '-', color='xkcd:lavender', label="Fit -511 keV")
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

## ***************************************************************************************************** ##
## Funtion to fit accumulation curve to experimental data, extracting total nr. of radioactive nuclei at ##
## the end of the irradiation (N_Dirr) for the SDD detector                                              ##
## ***************************************************************************************************** ##
def FitNpeakSDD(func, time, countsKa, errKa, countsKb, errKb, countsL, errL, init, efficiency, t_trans, lab, energy_key, radType):
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
    time     = np.array(time)
    countsKa = np.array(countsKa)
    countsKb = np.array(countsKb)
    countsL = np.array(countsL)

    ## Fit the data, passing radType explicitly    
    poptKa, pcovKa = curve_fit(lambda t, *p: Npeak(t, *p),
                               time, countsKa, p0=init[radType[0]][0:2], sigma=errKa[1:], absolute_sigma=True)
    
    poptKb, pcovKb = curve_fit(lambda t, *p: Npeak(t, *p), 
                               time, countsKb, p0=init[radType[1]][0:2], sigma=errKb[1:], absolute_sigma=True)
    
    poptL, pcovL = curve_fit(lambda t, *p: Npeak(t, *p), 
                            time, countsL, p0=init[radType[2]][0:2], sigma=errL[1:], absolute_sigma=True)
    
    ## Get fit parameters
    # Ka line
    N0Ka, N0Ka_err         = poptKa[0], np.sqrt(np.diag(pcovKa))[0] 
    bgRateKa, bgRateKa_err = poptKa[1], np.sqrt(np.diag(pcovKa))[1]
    # Kb line
    N0Kb, N0Kb_err         = poptKb[0], np.sqrt(np.diag(pcovKb))[0]
    bgRateKb, bgRateKb_err = poptKb[1], np.sqrt(np.diag(pcovKb))[1] 
    # L- lines
    N0L, N0L_err           = poptL[0], np.sqrt(np.diag(pcovL))[0]
    bgRateL, bgRateL_err   = poptL[1], np.sqrt(np.diag(pcovL))[1] 

    ## Constants
    halfLifeMin         = 2.8 * 60  # Decay half-life (minutes)
    halfLife_min_err    = 0.01*60 # minutes
    lambda_decay        = np.log(2) / halfLifeMin  # Decay constant
    lambda_decay_err    = np.log(2) * halfLife_min_err / halfLifeMin**2  # in min^-1
    t_trans_err         = 1. # minute

    ## Calculate N_Dirr and error propagation
    NdirrKa     = N0Ka/(efficiency[0][0] * np.exp(-lambda_decay*t_trans))
    NdirrKa_err = np.sqrt((np.exp(lambda_decay*t_trans)*N0Ka_err/efficiency[0][0])**2 + 
                          (N0Ka*np.exp(lambda_decay*t_trans)*efficiency[0][1]/efficiency[0][0]**2)**2 + 
                          (t_trans*N0Ka*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[0][0])**2 + 
                          (lambda_decay*N0Ka*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[0][0])**2)
    
    NdirrKb     = N0Kb/(efficiency[1][0] * np.exp(-lambda_decay*t_trans))
    NdirrKb_err = np.sqrt((np.exp(lambda_decay*t_trans)*N0Kb_err/efficiency[1][0])**2 + 
                          (N0Kb*np.exp(lambda_decay*t_trans)*efficiency[1][1]/efficiency[1][0]**2)**2 + 
                          (t_trans*N0Kb*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[1][0])**2 + 
                          (lambda_decay*N0Kb*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[1][0])**2)
    
    NdirrL     = N0L/(efficiency[2][0] * np.exp(-lambda_decay*t_trans))
    NdirrL_err = np.sqrt((np.exp(lambda_decay*t_trans)*N0L_err/efficiency[2][0])**2 + 
                          (N0L*np.exp(lambda_decay*t_trans)*efficiency[2][1]/efficiency[2][0]**2)**2 + 
                          (t_trans*N0L*np.exp(lambda_decay*t_trans)*lambda_decay_err/efficiency[2][0])**2 + 
                          (lambda_decay*N0L*np.exp(lambda_decay*t_trans)*t_trans_err/efficiency[2][0])**2)

    ## Print results
    """     print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e} | bgRate = ({bgRateKa:.2f} +- {bgRateKa_err:.2f}) counts/min")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e} | bgRate = ({bgRateKb:.2f} +- {bgRateKb_err:.2f}) counts/min")
    print(f"L lines: \t Ndirr = {NdirrL:.3e} +- {NdirrL_err:.0e} | bgRate = ({bgRateL:.2f} +- {bgRateL_err:.2f}) counts/min")
    print(f"Ka/Kb ratio = \t {(NdirrKa/NdirrKb):.2f}")
    print()
    """
    ## Create dictionaries for results
    N_D_irr_SDD = {
        energy_key: {
            "Ka": NdirrKa,
            "Kb": NdirrKb,
            "L-": NdirrL
        }
    }

    N_D_irr_SDD_err = {
        energy_key: {
            "Ka": NdirrKa_err,
            "Kb": NdirrKb_err,
            "L-": NdirrL_err
        }
    }

    ## Print dictionaries
    #  Nominal values
    for key, value in N_D_irr_SDD.items():
        print(f'    "{key}": {{"Ka": {value["Ka"]:.3e}, "Kb": {value["Kb"]:.3e}, "L": {value["L-"]:.3e}}},')
    #  Errors
    #for key, value in N_D_irr_SDD_err.items():
    #    print(f'    "{key}": {{"Ka": {value["Ka"]:.0e}, "Kb": {value["Kb"]:.0e}, "L": {value["L-"]:.0e}}},')

    ## Fit function for plotting
    fittedKa = Npeak(time, *poptKa)
    fittedKb = Npeak(time, *poptKb)
    fittedL  = Npeak(time, *poptL)

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.errorbar(time, countsKa, yerr=errKa[1:], fmt='^', color="xkcd:turquoise", label="$K_{\\alpha_{1,2,3}}$")
    ax.semilogy(time, fittedKa, '-', color="xkcd:green", label="Fit - $K_{\\alpha_{1,2,3}}$")
    ax.errorbar(time, countsKb, yerr=errKb[1:],fmt='v', color="xkcd:salmon", label="$K_{\\beta_{1,3}}$")
    ax.semilogy(time, fittedKb, '-', color="xkcd:magenta", label="Fit - $K_{\\beta_{1,3}}$")
    ax.errorbar(time, countsL, yerr=errL[1:],fmt='>', color="xkcd:orange", label="$L_{\\alpha,\\beta}$")
    ax.semilogy(time, fittedL, '-', color="xkcd:light orange", label="Fit - $L_{\\alpha,\\beta}$")
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel("Acquisition Time [minutes]", fontsize=22)
    ylabel("Accumulated Yield", fontsize=22)
    title("Accumulation Fit: "+lab, fontsize=24)
    show()

    return

## ***************************************************************************************************** ##
## Funtion to fit accumulation curve to SDD detector experimental data, extracting total nr. of          ##
## radioactive nuclei at the end of the irradiation (N_Dirr) and decay Half-Life, for the  data          ##
## ***************************************************************************************************** ##
def FitNpeakHalfLifeSDD(func, time, countsKa, errKa, countsKb, errKb, init, efficiency, t_trans, lab, energy_key, radType):
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
    time        = np.array(time)
    countsKa    = np.array(countsKa)
    countsKb    = np.array(countsKb)


    ## Fit the data, passing radType explicitly
    # Ka line
    poptKa, pcovKa          = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, countsKa, p0=init[radType[0]][0:2], sigma=errKa[1:], absolute_sigma=True)
    # Kb line
    poptKb, pcovKb          = curve_fit(lambda t, *p: NpeakHalfLife(t, t_trans, *p), 
                                        time, countsKb, p0=init[radType[1]][0:2], sigma=errKb[1:], absolute_sigma=True)
    
    ## Get fit parameters and std_dev = sqrt(variance) = sqrt(diag(cov))
    # Ka line 
    N0Ka, N0Ka_err                  = poptKa[0],    np.sqrt(np.diag(pcovKa))[0]
    lambdaKa, lambdaKa_err          = poptKa[1],    np.sqrt(np.diag(pcovKa))[1]
    # Kb line   
    N0Kb, N0Kb_err                  = poptKb[0],    np.sqrt(np.diag(pcovKb))[0]  
    lambdaKb, lambdaKb_err          = poptKb[1],    np.sqrt(np.diag(pcovKb))[1]

    ## Constants
    t_trans_err         = 1. # minute

    ## Calculate Half-Lifes from fitted lambdas
    ## Ka line
    hLifeMinKa        = np.log(2)/lambdaKa
    hLifeMinKa_err    = hLifeMinKa*lambdaKa_err/lambdaKa
    ## Kb line
    hLifeMinKb        = np.log(2)/lambdaKb
    hLifeMinKb_err    = hLifeMinKb*lambdaKb_err/lambdaKb

    ## Calculate N_Dirr and error propagation
    ## Ka line
    NdirrKa         = N0Ka/efficiency[0][0]
    NdirrKa_err     = np.sqrt((np.exp(lambdaKa*t_trans)*N0Ka_err/efficiency[0][0])**2 + 
                            (N0Ka*np.exp(lambdaKa*t_trans)*efficiency[0][1]/efficiency[0][0]**2)**2 + 
                            (t_trans*N0Ka*np.exp(lambdaKa*t_trans)*lambdaKa_err/efficiency[0][0])**2 + 
                            (lambdaKa*N0Ka*np.exp(lambdaKa*t_trans)*t_trans_err/efficiency[0][0])**2)
    ## Kb line
    NdirrKb         = N0Kb/efficiency[1][0]
    NdirrKb_err     = np.sqrt((np.exp(lambdaKb*t_trans)*N0Kb_err/efficiency[1][0])**2 + 
                            (N0Kb*np.exp(lambdaKb*t_trans)*efficiency[1][1]/efficiency[1][0]**2)**2 + 
                            (t_trans*N0Kb*np.exp(lambdaKb*t_trans)*lambdaKb_err/efficiency[1][0])**2 + 
                            (lambdaKb*N0Kb*np.exp(lambdaKb*t_trans)*t_trans_err/efficiency[1][0])**2)
    
    ## Print results
    print("******************************"+len(lab)*"*")
    print(f"* Accumulation fit results: {lab} *")
    print("******************************"+len(lab)*"*")
    print(f"Ka line: \t Ndirr = {NdirrKa:.3e} +- {NdirrKa_err:.0e} | Half-Life = ({(hLifeMinKa/60):.2f} +- {(hLifeMinKa_err/60):.2f}) hours")
    print(f"Kb line: \t Ndirr = {NdirrKb:.3e} +- {NdirrKb_err:.0e} | Half-Life = ({(hLifeMinKb/60):.2f} +- {(hLifeMinKb_err/60):.2f}) hours")
    print(f"Ka/Kb = {(NdirrKa/NdirrKb):.2f}")
    print()

    ## Fited function for plotting
    fittedKa    = NpeakHalfLife(time, t_trans, *poptKa)
    fittedKb    = NpeakHalfLife(time, t_trans, *poptKb)

    # Plot the results
    fig, ax = plt.subplots()
    ax.set_yscale("log")
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