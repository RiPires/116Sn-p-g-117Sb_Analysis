###########################################################
## Script to plot SDD accumulation at different energies ##
###########################################################

## -------------------------- ##
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different beam energy decay run files
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/',
            '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved_LiveTime/SDD/']

## Define initial guess of N0, bgRate for each beam energy
##                  [[    Ka   ], [    Kb   ]] 
initParamsDict = {
    'Ebeam=3.2MeV': {"Ka": (1.0e6, 1.), "Kb": (2.5e6, 1.)},  
    'Ebeam=3.5MeV': {"Ka": (1.2e6, 1.), "Kb": (2.5e6, 1.)},  
    'Ebeam=3.9MeV': {"Ka": (3.0e6, 1.), "Kb": (6.0e6, 1)}, 
    'Ebeam=4.3MeV': {"Ka": (5.0e6, 1.), "Kb": (1.0e7, 1.)},  
    'Ebeam=4.7MeV': {"Ka": (1.0e7, 1.), "Kb": (2.0e7, 1.)},  
    'Ebeam=5.0MeV': {"Ka": (2.0e7, 1.), "Kb": (4.0e7, 1.)}}

## Convoluted efficiency for each energy
## Parameters for the detector at mean position of (12+9)/2 mm
efficiency_params = {
'Ebeam=3.2MeV': {'Ka': (1.865e-3, 5e-4), 'Kb': (2.472e-4, 6e-5)},
'Ebeam=3.5MeV': {'Ka': (1.877e-3, 5e-4), 'Kb': (2.369e-4, 6e-5)},
'Ebeam=3.9MeV': {'Ka': (1.867e-3, 5e-4), 'Kb': (2.397e-4, 6e-5)},
'Ebeam=4.3MeV': {'Ka': (1.873e-3, 5e-4), 'Kb': (2.394e-4, 6e-5)},
'Ebeam=4.7MeV': {'Ka': (1.869e-3, 5e-4), 'Kb': (2.366e-4, 5e-5)},
'Ebeam=5.0MeV': {'Ka': (1.890e-3, 5e-4), 'Kb': (2.421e-4, 6e-5)}}

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
    radType = ["Ka", "Kb"]

    ## Get efficiency and emission probability for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        epsilonD = [efficiency_params[energy_key][rad] for rad in radType]
        t_transMin = t_transMin_key[energy_key]
    except KeyError:
        raise ValueError(f"Invalid energy '{energy_key}' or radType '{radType}'. Check input values.")

    ## Warning message
    if energy_key is None:
        print(f"Warning: No initial parameters found for {files}. Using default values.")
        initParamsNpeak = [[1.2e6], [2.8e5]]  # Default values
    else:
        initParamsNpeak = initParamsDict[energy_key]  # Get the correct values

    ## Extract accumulation data from the run files
    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_time = AccumulateSDD_BgRemoved(files)

    ## Fit the data to the Npeak curve
    FitNpeakSDD(Npeak,  accu_time, accu_Ka, accu_Ka_err, 
                        accu_Kb, accu_Kb_err, 
                        initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                        energy_key=energy_key, radType=radType, 
                        lab=str(files[15:27]+' - '+files[-4:-1]+' @ CNA'))