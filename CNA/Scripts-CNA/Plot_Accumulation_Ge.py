############################################################
## Script to plot HPGe accumulation at different energies ##
############################################################

## -------------------------- ##
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different activation beam energies
gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/']

## Define initial guess N_Dirr for each beam energy

initParamsDict = {##          (N0,bgRate),       (N0,bgRate),       (N0,bgRate),           (N0,bgRate) 
    'Ebeam=3.2MeV': {"gamma": (1.0e7, 1.), "Ka": (1.0e7, 1.), "Kb": (2.5e7, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)},
    'Ebeam=3.5MeV': {"gamma": (1.2e7, 1.), "Ka": (1.2e7, 1.), "Kb": (2.5e8, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)}, 
    'Ebeam=3.9MeV': {"gamma": (3.0e8, 1.), "Ka": (3.0e8, 1.), "Kb": (6.0e8, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)},  
    'Ebeam=4.3MeV': {"gamma": (5.0e8, 1.), "Ka": (5.0e8, 1.), "Kb": (1.0e8, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)},  
    'Ebeam=4.7MeV': {"gamma": (1.0e8, 1.), "Ka": (1.0e8, 1.), "Kb": (2.0e8, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)},  
    'Ebeam=5.0MeV': {"gamma": (2.0e9, 1.), "Ka": (2.0e9, 1.), "Kb": (4.0e9, 1.), "511keV": (1e7, 1.), "861keV": (1e7, 1.), "1004keV": (1e7, 1.)}}

## Efficiency and emission probabilities for each energy
efficiency_params = { ##  ( eff  , err )         ( eff  , err )         ( eff  , err )             ( eff    , err )            ( eff    , err )             
'Ebeam=3.2MeV': {'gamma': (0.1562, 0.006), 'Ka': (0.1488, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.645e-4, 1e-5), "861keV": (9.300e-5, 1e-6), "1004keV": (7.745e-5, 3e-6)},
'Ebeam=3.5MeV': {'gamma': (0.1562, 0.006), 'Ka': (0.1490, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.596e-4, 2e-5), "861keV": (9.470e-5, 4e-7), "1004keV": (7.320e-5, 4e-6)},
'Ebeam=3.9MeV': {'gamma': (0.1562, 0.006), 'Ka': (0.1488, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.761e-4, 1e-5), "861keV": (9.130e-5, 4e-6), "1004keV": (7.650e-5, 3e-6)},
'Ebeam=4.3MeV': {'gamma': (0.1562, 0.006), 'Ka': (0.1489, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.713e-4, 1e-5), "861keV": (9.075e-5, 4e-6), "1004keV": (7.590e-5, 5e-6)},
'Ebeam=4.7MeV': {'gamma': (0.1561, 0.006), 'Ka': (0.1489, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.559e-4, 2e-5), "861keV": (9.330e-5, 3e-7), "1004keV": (7.600e-5, 2e-6)},
'Ebeam=5.0MeV': {'gamma': (0.1562, 0.006), 'Ka': (0.1489, 0.003), 'Kb': (0.0324, 0.001), "511keV": (9.543e-4, 3e-5), "861keV": (9.070e-5, 2e-7), "1004keV": (7.730e-5, 5e-6)}}

## Transportation time (in minutes) for each activation energy
t_transMin_key ={'Ebeam=3.2MeV': 63,
                 'Ebeam=3.5MeV': 29,
                 'Ebeam=3.9MeV': 32,
                 'Ebeam=4.3MeV': 40,
                 'Ebeam=4.7MeV': 31,
                 'Ebeam=5.0MeV': 29}
    
## Loop over different activation energies
for files in gePaths:

    ## Extract energy value from path
    energy_key = next((key for key in initParamsDict if key in files), None)
    radType = ["gamma", "Ka", "Kb", "511keV", "861keV", "1004keV"]

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
        initParamsNpeak = [[1.2e6], [1.2e6], [2.8e5]]  # Default values
    else:
        initParamsNpeak = initParamsDict[energy_key]  # Get the correct values

    ## Extract accumulation data from the run files
    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_gamma, accu_gamma_err, accu_511, accu_511_err, accu_861, accu_861_err, accu_1004, accu_1004_err, accu_time = AccumulateGe_BgRemove(files)

    ## Fit the data for Npeak
    FitNpeakHPGe(Npeak, accu_time, accu_gamma, accu_gamma_err, 
                        accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_511, accu_511_err, accu_861, accu_861_err, accu_1004, accu_1004_err,
                        initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                        energy_key=energy_key, radType=radType, 
                        lab=str(files[15:27]+' - '+files[-5:-1]+' @ CNA'))