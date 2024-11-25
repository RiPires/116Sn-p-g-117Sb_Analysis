#################### RiP ############################
## Funtion to fit Double gaussian                  ##
#####################################################

## ------------------------------- ##
from __future__ import print_function 
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from include.ReadData import *
## ------------------------------- ##

def double_gaussian(x, params):
    (c1, mu1, sigma1, c2, mu2, sigma2) = params
    x = np.array(x)
    res =   c1 * np.exp( - (x - mu1)**2.0 / (2.0 * sigma1**2.0) ) \
          + c2 * np.exp( - (x - mu2)**2.0 / (2.0 * sigma2**2.0) )
    return res

def double_gaussian_fit(params, x, y):
    fit = double_gaussian(x, params)
    return (fit - y)
###  --------------------------------------------------------------  ###

## Path to calibration file
calibFile152Eu = "../Calibrations/SDD/CalibrationRuns_PosExp/Run14_152Eu_detSDD_2mm.mca"

## Channel list
channels152Eu = MCA2Lists(calibFile152Eu)[1]
## Calibration yield list of sources
calibYield152Eu = MCA2Lists(calibFile152Eu)[0]

# Initial guesses for the parameters
initial_params = [
    48, 1458, 1,  # Parameters for the first Gaussian
    21, 1497, 1   # Parameters for the second Gaussian
]

# Perform the fit
fit_params, _ = leastsq(double_gaussian_fit, initial_params, args=(channels152Eu, calibYield152Eu))

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(channels152Eu, calibYield152Eu, '.-', label="Data", color="blue")
plt.plot(channels152Eu, double_gaussian(channels152Eu, fit_params), label="Fit", color="red", lw=2)
plt.xlabel("Channels")
plt.ylabel("Counts")
plt.legend()
plt.title("Double Gaussian Fit")
plt.show()

# Print fitted parameters
print("Fitted Parameters:")
print(f"c1: {fit_params[0]:.2f}, mu1: {fit_params[1]:.2f}, sigma1: {fit_params[2]:.2f}")
print(f"c2: {fit_params[3]:.2f}, mu2: {fit_params[4]:.2f}, sigma2: {fit_params[5]:.2f}")