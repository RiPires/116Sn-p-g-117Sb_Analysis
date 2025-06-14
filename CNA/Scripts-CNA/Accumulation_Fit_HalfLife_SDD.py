###########################################################
## Script to perform SDD accumulation fit, at different  ##
## energies extracting N0 and decay Half-Life values     ##
###########################################################

## -------------------------------- ##
from include.Accumulation import *
from include.Fits import *
## -------------------------------- ##

## Paths for different beam energy decay run files
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/']

## Define initial guess of (N0, lambda_min, bgRate) for each beam energy
initParamsDict = {
    'Ebeam=3.2MeV': {"Ka": (1.0e6, 4.126e-3, 1.0), "Kb": (2.5e6, 4.126e-3, 1.0), "L-": (1.0e6, 4.126e-3, 1.0)},  
    'Ebeam=3.5MeV': {"Ka": (1.2e6, 4.126e-3, 1.0), "Kb": (2.5e6, 4.126e-3, 1.0), "L-": (2.0e6, 4.126e-3, 1.0)},  
    'Ebeam=3.9MeV': {"Ka": (3.0e6, 4.126e-3, 1.0), "Kb": (6.0e6, 4.126e-3, 1.0), "L-": (5.0e6, 4.126e-3, 1.0)}, 
    'Ebeam=4.3MeV': {"Ka": (5.0e6, 4.126e-3, 1.0), "Kb": (1.0e7, 4.126e-3, 1.0), "L-": (1.0e7, 4.126e-3, 1.0)},  
    'Ebeam=4.7MeV': {"Ka": (1.0e7, 4.126e-3, 1.0), "Kb": (2.0e7, 4.126e-3, 1.0), "L-": (2.0e7, 4.126e-3, 1.0)},  
    'Ebeam=5.0MeV': {"Ka": (2.0e7, 4.126e-3, 1.0), "Kb": (4.0e7, 4.126e-3, 1.0), "L-": (4.0e7, 4.126e-3, 1.0)}}

## Convoluted efficiency for and uncetainty for each energy
## Parameters for the detector at mean position of (12+9)/2 mm  ## VERIFICAR POSIÇÕES E VALORES !!!
efficiency_params = {
    'Ebeam=3.2MeV': {'Ka': (1.884e-03, 5e-04), 'Kb': (2.345e-04, 5e-05), 'L-': (6.626e-04, 2e-04)},
    'Ebeam=3.5MeV': {'Ka': (1.870e-03, 4e-04), 'Kb': (2.320e-04, 5e-05), 'L-': (6.602e-04, 2e-04)},
    'Ebeam=3.9MeV': {'Ka': (1.863e-03, 5e-04), 'Kb': (2.357e-04, 6e-05), 'L-': (6.628e-04, 2e-04)},
    'Ebeam=4.3MeV': {'Ka': (1.883e-03, 5e-04), 'Kb': (2.295e-04, 5e-05), 'L-': (6.614e-04, 2e-04)},
    'Ebeam=4.7MeV': {'Ka': (1.882e-03, 5e-04), 'Kb': (2.336e-04, 5e-05), 'L-': (6.452e-04, 2e-04)},
    'Ebeam=5.0MeV': {'Ka': (1.857e-03, 5e-04), 'Kb': (2.317e-04, 6e-05), 'L-': (6.377e-04, 2e-04)}}

## Transportation time (in minutes) for each activation energy
t_transMin_key ={'Ebeam=3.2MeV': 27,
                 'Ebeam=3.5MeV': 28,
                 'Ebeam=3.9MeV': 31,
                 'Ebeam=4.3MeV': 39,
                 'Ebeam=4.7MeV': 30,
                 'Ebeam=5.0MeV': 28}

## Loop over different activation energies
for files in sddPaths:
    
    ## Extract energy value from path
    energy_key = next((key for key in initParamsDict if key in files), None)
    radType = ["Ka", "Kb", "L-"]

    ## Get the convoluted efficiency for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        epsilonD = [efficiency_params[energy_key][rad] for rad in radType]
        t_transMin = t_transMin_key[energy_key]
    except KeyError:
        raise ValueError(f"Invalid energy '{energy_key}' or radType '{radType}'. Check input values.")

    ## Set values for initial parameters
    initParamsNpeak = initParamsDict[energy_key]

    ## Extract accumulation data from the run files
    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_L, accu_L_err, accu_time = AccumulateSDD_BgRemoved(files)

    ## Fit the data to the Npeak curve
    FitNpeakHalfLifeSDD(NpeakHalfLife, accu_time, accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_L, accu_L_err, 
                        initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                        energy_key=energy_key, radType=radType, 
                        lab=str(files[15:27]+' - '+files[-4:-1]+' @ CNA'))