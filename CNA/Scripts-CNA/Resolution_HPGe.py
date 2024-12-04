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
    return a/E + b/np.sqrt(E) + c

# Example experimental data (replace with your actual data)
E = np.array([0.1218,
0.2447,
0.3443,
0.4111,
0.4440,
0.7789,
0.8674,
0.9641,
1.0858,
1.1121,
0.0810,
0.2764,
0.3029,
0.3560,
0.3839,
0.0321,
0.0367,
0.6617,
1.1732])  # Energies (MeV)

FWHM = np.array([0.0005,   
0.0005,   
0.0006,   
0.0007,   
0.0007,   
0.0008,   
0.0009,   
0.0009,   
0.0009,   
0.0009,   
0.0005,   
0.0005,   
0.0005,   
0.0006,   
0.0006,   
0.0005,
0.0006,
0.0007,   
0.0009])  # FWHM values

R = FWHM / E  # Calculate resolution

R_err = np.array([0.00006,
0.00012,
0.00004,
0.00028,
0.00019,
0.00007,
0.00017,
0.00007,
0.00008,
0.00007,
0.00038,
0.00011,
0.00005,
0.00002,
0.00004,
0.00118,
0.00352,
0.00002,
0.00004])

# Perform the fit, including uncertainties in R
popt, pcov = curve_fit(resolution_model, E, R, p0=[0.0005,-0.0005,0.001], sigma=R_err, absolute_sigma=True)

## Residuals
residuals = R - resolution_model(E, *popt)
## Residual sum of squares
ss_res = np.sum(residuals**2)
## Total sum of suqares
ss_tot = np.sum((R-np.mean(R))**2)
## R squared
r_squared = 1 - (ss_res / ss_tot)

# Extract fitting parameters and their uncertainties
a, b, c = popt
a_err, b_err, c_err = np.sqrt(np.diag(pcov))

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
ax.errorbar(1/np.sqrt(E), R, yerr=R_err, color='blue', fmt='o', label="HPGe Resolution")
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
ax.errorbar(1/np.sqrt(E), R, yerr=R_err, fmt='o', label="HPGe", color='blue', capsize=3)
ax.plot(E_fit, R_fit, label="Fit: $R(E) = \\frac{a}{E} + \\frac{b}{\\sqrt{E}} + c$", color='red')
legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel("1/$\\sqrt{\\rm{E}}$  [Energy (MeV)]", fontsize=22)
ylabel("R = $\\frac{\\rm{FWHM}}{\\rm{E}}$", fontsize=22)
show()