############################################################
## Script to plot HPGe accumulation at different energies ##
############################################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different activation beam energies
gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved_LiveTime/HPGe/',]

## Define initial guess N_Dirr for each beam energy
##                  [[gamma], [ Ka  ], [ Kb  ]] 
initParamsDict = {
    'Ebeam=3.2MeV': [[1.0e6, 1.], [1.0e6, 1.], [2.5e6, 1.]],  # Example values for 3.2 MeV
    'Ebeam=3.5MeV': [[1.2e6, 1.], [1.2e6, 1.], [2.5e7, 1.]],  # Example values for 3.5 MeV
    'Ebeam=3.9MeV': [[3.0e7, 1.], [3.0e7, 1.], [6.0e7, 1.]],  # Example values for 3.9 MeV
    'Ebeam=4.3MeV': [[5.0e7, 1.], [5.0e7, 1.], [1.0e7, 1.]],  # Example values for 4.3 MeV
    'Ebeam=4.7MeV': [[1.0e7, 1.], [1.0e7, 1.], [2.0e7, 1.]],  # Example values for 4.7 MeV
    'Ebeam=5.0MeV': [[2.0e8, 1.], [2.0e8, 1.], [4.0e8, 1.]],  # Example values for 5.0 MeV
}

## Loop over different activation energies
for files in gePaths:
    ## Extract energy value from path
    energy_key = next((key for key in initParamsDict if key in files), None)

    if energy_key is None:
        print(f"Warning: No initial parameters found for {files}. Using default values.")
        initParamsNpeak = [[1.2e6], [1.2e6], [2.8e5]]  # Default values
    else:
        initParamsNpeak = initParamsDict[energy_key]  # Get the correct values

    ## Extract accumulation data from the run files
    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_gamma, accu_gamma_err, accu511, accu_time = AccumulateGe_BgRemove(files)

    ## Fit the data for Npeak
    FitNpeakHPGe(NpeakHPGe, accu_time, accu_gamma, accu_gamma_err, 
                        accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, 
                        initParamsNpeak, energy_key=energy_key, 
                        lab=str(files[15:27]+' - '+files[-5:-1]))