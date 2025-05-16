import numpy as np

## ----------- Cross-Section Calculation ------------- ##
def compute_cross_section(N_D, N_D_err, ruth, ruth_err, t_irr, Np, decayConstant, epsilon_p, t_irr_err, decayConstant_err):
    decayFactor = 1 - np.exp(-decayConstant * t_irr)
    sigma = ruth * (4 * np.pi * N_D * epsilon_p) * decayConstant * t_irr / (decayFactor * Np)

    decay_term = np.exp(decayConstant * t_irr)
    decay_sens_t = (decayConstant * decay_term * (-decayConstant * t_irr + decay_term - 1) / (decay_term - 1)**2)
    decay_sens_lambda = (t_irr * decay_term * (-decayConstant * t_irr + decay_term - 1) / (decay_term - 1)**2)

    err_sq = ((sigma / ruth * ruth_err)**2 +
              sigma**2 / Np +
              (sigma / N_D)**2 * N_D_err**2 +
              (decay_sens_t * (4 * np.pi * epsilon_p * N_D * ruth / Np))**2 * t_irr_err**2 +
              (decay_sens_lambda * (4 * np.pi * epsilon_p * N_D * ruth / Np))**2 * decayConstant_err**2)

    return sigma, np.sqrt(err_sq)