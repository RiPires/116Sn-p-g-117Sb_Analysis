################################################################
## Script for calculating quadratic resolution fit parameters ##
################################################################

## ----------------------------------- ##
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.pylab import *
## ----------------------------------- ##

# Define the resolution response model
def resolution_model(E, a, b, c):
    return a/E + b / np.sqrt(E) + c

# Example experimental data (replace with your actual data)
E = np.array([0.0043, 0.0046,  0.0049, 0.0053, 0.0310, 0.0358, 0.0056, 0.0062, 0.0066, 0.0072, 0.0395, 0.0401, 0.0454])  # Energies (MeV)
FWHM = np.array([0.00013, 0.00016, 0.00018, 0.00016, 0.00032, 0.00035, 0.00014, 0.00017, 0.00021, 0.00019, 0.00037, 0.00036, 0.00044])  # FWHM values
R = FWHM / E  # Calculate resolution
R_err = np.array([0.00068, 0.00158, 0.00385, 0.00166, 0.00054, 0.00002, 0.00052, 0.00118, 0.00322, 0.00183, 0.00043, 0.00024, 0.00061])

# Perform the fit, including uncertainties in R
popt, pcov = curve_fit(resolution_model, E, R, sigma=R_err, absolute_sigma=False)

# Extract fitting parameters and their uncertainties
a, b, c = popt
a_err, b_err, c_err = np.sqrt(np.diag(pcov))

## Residuals
residuals = R - resolution_model(E, *popt)
## Residual sum of squares
ss_res = np.sum(residuals**2)
## Total sum of suqares
ss_tot = np.sum((R-np.mean(R))**2)
## R squared
r_squared = 1 - (ss_res / ss_tot)

# Print the results
print(f"Fitting Parameters:")
print(f"a = {a:.4f} ± {a_err:.4f}")
print(f"b = {b:.4f} ± {b_err:.4f}")
print(f"c = {c:.4f} ± {c_err:.4f}")
print("r_squared = ", r_squared)

# Plot the results
E_fit = np.linspace(min(1/np.sqrt(E)), max(1/np.sqrt(E)), 500)  # Fine grid for plotting
R_fit = resolution_model((1/E_fit)**2, *popt)

fig, ax = plt.subplots()
ax.errorbar(1/np.sqrt(E), R, yerr=R_err, color='blue', fmt='o', label="SDD")
ax.plot(E_fit, R_fit, color='red', label="Fit: $R(E) = \\frac{a}{E} + \\frac{b}{\\sqrt{E}} + c$")
legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel("1/$\\sqrt{\\rm{E}}$  [Energy (MeV)]", fontsize=22)
ylabel("R = $\\frac{\\rm{FWHM}}{\\rm{E}}$", fontsize=22)
show()

###########################
### USING NUMPY POLYFIT ###
###########################
coef, cova = np.polyfit(1/np.sqrt(E), R, 2, rcond=None, full=False, w=None, cov=True)
a, b, c = coef
a_err, b_err, c_err = np.sqrt(np.diag(pcov))

## Residuals
residuals = R - resolution_model(E, a, b, c)
## Residual sum of squares
ss_res = np.sum(residuals**2)
## Total sum of suqares
ss_tot = np.sum((R-np.mean(R))**2)
## R squared
r_squared = 1 - (ss_res / ss_tot)

# Print the results
print(f"Fitting Parameters:")
print(f"a = {a:.4f} ± {a_err:.4f}")
print(f"b = {b:.4f} ± {b_err:.4f}")
print(f"c = {c:.4f} ± {c_err:.4f}")
print("r_squared = ", r_squared)

# Plot the results
E_fit = np.linspace(min(1/np.sqrt(E)), max(1/np.sqrt(E)), 500)  # Fine grid for plotting
R_fit = resolution_model((1/E_fit)**2, a, b, c)

fig, ax = plt.subplots()
ax.errorbar(1/np.sqrt(E), R, yerr=R_err, fmt='o', color='blue', label="SDD Resolution")
ax.plot(E_fit, R_fit, color='red', label="Fit: $R(E) = \\frac{a}{E} + \\frac{b}{\\sqrt{E}} + c$")
legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel("1/$\\sqrt{\\rm{E}}$  [Energy (MeV)]", fontsize=22)
ylabel("R = $\\frac{\\rm{FWHM}}{\\rm{E}}$", fontsize=22)
show()