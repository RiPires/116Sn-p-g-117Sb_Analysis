############################################################
## Script to perform HPGe accumulation fit, at different  ##
## energies extracting N0 and decay Half-Life values      ##
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

## Define initial guess of (N0, lambda_min) for each beam energy
initParamsDict = {
    'Ebeam=3.2MeV': {"gamma": (1.0e7, 4.126e-3), "Ka": (1.0e7, 4.126e-3), "Kb": (2.5e7, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)},
    'Ebeam=3.5MeV': {"gamma": (1.2e7, 4.126e-3), "Ka": (1.2e7, 4.126e-3), "Kb": (2.5e8, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)}, 
    'Ebeam=3.9MeV': {"gamma": (3.0e8, 4.126e-3), "Ka": (3.0e8, 4.126e-3), "Kb": (6.0e8, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)},  
    'Ebeam=4.3MeV': {"gamma": (5.0e8, 4.126e-3), "Ka": (5.0e8, 4.126e-3), "Kb": (1.0e8, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)},  
    'Ebeam=4.7MeV': {"gamma": (1.0e8, 4.126e-3), "Ka": (1.0e8, 4.126e-3), "Kb": (2.0e8, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)},  
    'Ebeam=5.0MeV': {"gamma": (2.0e9, 4.126e-3), "Ka": (2.0e9, 4.126e-3), "Kb": (4.0e9, 4.126e-3), "511keV": (1e7, 4.126e-3), "861keV": (1e7, 4.126e-3), "1004keV": (1e7, 4.126e-3)}}

## Convoluted efficiency and error values for each beam energy, and radiation type
efficiency_params = {             
'Ebeam=3.2MeV': {'gamma': (0.1221, 0.005), 'Ka': (0.1270, 0.004), 'Kb': (0.0275, 0.001), "511keV": (8.458e-4, 3e-5), "861keV": (8.055e-5, 2e-6), "1004keV": (5.695e-5, 6e-6)},
'Ebeam=3.5MeV': {'gamma': (0.1222, 0.005), 'Ka': (0.1268, 0.004), 'Kb': (0.0274, 0.001), "511keV": (8.286e-4, 1e-5), "861keV": (7.800e-5, 4e-7), "1004keV": (5.735e-5, 4e-6)},
'Ebeam=3.9MeV': {'gamma': (0.1220, 0.005), 'Ka': (0.1267, 0.004), 'Kb': (0.0274, 0.001), "511keV": (8.428e-4, 1e-5), "861keV": (7.865e-5, 4e-6), "1004keV": (5.570e-5, 3e-6)},
'Ebeam=4.3MeV': {'gamma': (0.1222, 0.005), 'Ka': (0.1268, 0.004), 'Kb': (0.0274, 0.001), "511keV": (8.415e-4, 1e-5), "861keV": (7.625e-5, 4e-6), "1004keV": (5.950e-5, 5e-6)},
'Ebeam=4.7MeV': {'gamma': (0.1222, 0.005), 'Ka': (0.1269, 0.004), 'Kb': (0.0275, 0.001), "511keV": (8.507e-4, 2e-5), "861keV": (7.825e-5, 3e-7), "1004keV": (5.865e-5, 2e-6)},
'Ebeam=5.0MeV': {'gamma': (0.1220, 0.005), 'Ka': (0.1268, 0.004), 'Kb': (0.0274, 0.001), "511keV": (8.343e-4, 3e-5), "861keV": (8.035e-5, 2e-7), "1004keV": (6.200e-5, 5e-6)}}

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

    ## Get the convoluted efficiency for the given energy and radiation type
    ## and the corresponding trasportation time
    try:
        epsilonD = [efficiency_params[energy_key][rad] for rad in radType]
        t_transMin = t_transMin_key[energy_key]
    except KeyError:
        raise ValueError(f"Invalid energy '{energy_key}' or radType '{radType}'. Check input values.")

    ## Set initial parameters
    initParamsNpeak = initParamsDict[energy_key]

    ## Extract accumulation data from the run files
    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_gamma, accu_gamma_err, accu_511, accu_511_err, accu_861, accu_861_err, accu_1004, accu_1004_err, accu_time = AccumulateGe_BgRemove(files)

    ## Fit the data for Npeak
    FitNpeakHalfLifeHPGe(NpeakHalfLife, accu_time, accu_gamma, accu_gamma_err, accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, 
                         accu_511, accu_511_err, accu_861, accu_861_err, accu_1004, accu_1004_err,
                         initParamsNpeak, efficiency=epsilonD, t_trans=t_transMin,
                         energy_key=energy_key, radType=radType, 
                         lab=str(files[15:27]+' - '+files[-5:-1]+' @ CNA'))