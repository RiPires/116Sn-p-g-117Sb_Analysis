###########################################################
## Script to plot SDD accumulation at different energies ##
###########################################################

## -------------------------- ##
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different beam energy decay run files
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved/SDD/',
            '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved/SDD/',
            '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved/SDD/',
            '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved/SDD/',
            '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved/SDD/',
            '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved/SDD/']

## Define initial guess of (N0, bgRate) for each beam energy
initParamsDict = {
    'Ebeam=3.2MeV': {"Ka": (1.0e6, 1.), "Kb": (2.5e6, 1.), "L-": (1.0e6, 1.)},  
    'Ebeam=3.5MeV': {"Ka": (1.2e6, 1.), "Kb": (2.5e6, 1.), "L-": (2.0e6, 1.)},  
    'Ebeam=3.9MeV': {"Ka": (3.0e6, 1.), "Kb": (6.0e6, 1.), "L-": (5.0e6, 1.)}, 
    'Ebeam=4.3MeV': {"Ka": (5.0e6, 1.), "Kb": (1.0e7, 1.), "L-": (1.0e7, 1.)},  
    'Ebeam=4.7MeV': {"Ka": (1.0e7, 1.), "Kb": (2.0e7, 1.), "L-": (2.0e7, 1.)},  
    'Ebeam=5.0MeV': {"Ka": (2.0e7, 1.), "Kb": (4.0e7, 1.), "L-": (4.0e7, 1.)}}

## Convoluted efficiency for and uncetainty for each energy
## Parameters for the detector at mean position of (11+10)/2 mm  ## VERIFICAR POSIÇÕES E VALORES !!!
efficiency_params = {
    'Ebeam=3.2MeV': {'Ka': (1.873e-03, 5e-04), 'Kb': (2.317e-04, 6e-05), 'L-': (6.065e-04, 2e-04)},
    'Ebeam=3.5MeV': {'Ka': (1.874e-03, 5e-04), 'Kb': (2.315e-04, 5e-05), 'L-': (6.109e-04, 2e-04)},
    'Ebeam=3.9MeV': {'Ka': (1.877e-03, 5e-04), 'Kb': (2.335e-04, 6e-05), 'L-': (6.145e-04, 2e-04)},
    'Ebeam=4.3MeV': {'Ka': (1.877e-03, 5e-04), 'Kb': (2.322e-04, 6e-05), 'L-': (6.094e-04, 2e-04)},
    'Ebeam=4.7MeV': {'Ka': (1.875e-03, 5e-04), 'Kb': (2.329e-04, 6e-05), 'L-': (5.937e-04, 2e-04)},
    'Ebeam=5.0MeV': {'Ka': (1.871e-03, 5e-04), 'Kb': (2.327e-04, 6e-05), 'L-': (5.799e-04, 1e-04)}}

## Transportation time (in minutes) for each activation energy
t_transMin_key ={'Ebeam=3.2MeV': 28,
                 'Ebeam=3.5MeV': 29,
                 'Ebeam=3.9MeV': 32,
                 'Ebeam=4.3MeV': 40,
                 'Ebeam=4.7MeV': 31,
                 'Ebeam=5.0MeV': 29}

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

    ## Fit the data to the Npeak curve with linear trend
    FitNpeakSDD(Npeak,  accu_time, accu_Ka, accu_Ka_err, 
                        accu_Kb, accu_Kb_err, accu_L, accu_L_err,
                        initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                        energy_key=energy_key, radType=radType, 
                        lab=str(files[15:27]+' - '+files[-4:-1]+' @ CNA'))
    
"""     ## Fit the data to the Npeak curve without linear trend
    FitNpeakNoLinSDD(NpeakNoLin,  accu_time, accu_Ka, accu_Ka_err, 
                        accu_Kb, accu_Kb_err, accu_L, accu_L_err,
                        initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                        energy_key=energy_key, radType=radType, 
                        lab=str(files[15:27]+' - '+files[-4:-1]+' @ CNA')) """