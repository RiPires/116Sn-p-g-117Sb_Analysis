#################### RiP #################################
## Funtion to fit Gaussian, Lorentzian and Voigt curves ##
##########################################################

## ------------------------------- ##
from __future__ import print_function 
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
## ------------------------------- ##

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

# Define the Gaussian function
def gaussian(x, amp, mean, sigma):
    return amp * np.exp(-((x - mean) ** 2) / (2 * sigma ** 2))

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

    
def FitData(func, x, y, init, lab, roid, roiu):

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
            popt, _ = curve_fit(func, x_roi, y_roi, p0=p0)
            fitted_params.append(popt)

            # Add current fit to the combined result
            all_fits += gaussian(x, *popt)

            # Write results to file
            amp, mean, sigma = popt
            outFile.write(f"{mean:.2f}\t{sigma:.2f}\n")

    # Print results
    for i, param in enumerate(fitted_params, start=1):
        print(f"Peak {i}: Amplitude = {param[0]:.2f}, Mean = {param[1]:.2f}, Sigma = {param[2]:.2f}")

    # Plot the results
    plt.plot(x, y, label=f"Data ({lab})", color="blue")
    plt.plot(x, all_fits, label="Combined Fit", color="red", linestyle="--")
    plt.xlabel("Channel")
    plt.ylabel("Yield")
    plt.legend()
    plt.title("Gaussian Fit")
    plt.show()

    return fitted_params

def FitNGauss(func, x, y, init, lab):

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

    # Display the results
    print("Fitted Parameters for Each Gaussian Peak:")
    for i, (amp, mean, std_dev) in enumerate(zip(amplitudes, means, std_devs), start=1):
        print(f"Peak {i}: Amplitude = {amp:.2f}, Mean = {mean:.2f}, Std Dev = {std_dev:.2f}")

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Data", color='blue', linewidth=2)
    plt.plot(x, nGaussian(x, *popt), label="Fit", color='red', linewidth=2)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title(f"Fit for {n_peaks} Gaussian Peaks")
    plt.show()