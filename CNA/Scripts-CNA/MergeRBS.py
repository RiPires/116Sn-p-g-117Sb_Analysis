###########################################################
## Script to plotmerged  RBS spectra for each activation ##
###########################################################

## --------------------------- ##
import os
from include.PlotData import *
from include.ReadData import *
## --------------------------- ##


## Paths for each activation energy
Paths = {
    "Ebeam=3.2MeV": "../Activations/Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/RBS/",
    "Ebeam=3.5MeV": "../Activations/Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/RBS/",
    "Ebeam=3.9MeV": "../Activations/Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/RBS/",
    "Ebeam=4.3MeV": "../Activations/Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/RBS/",
    "Ebeam=4.7MeV": "../Activations/Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/RBS/",
    "Ebeam=5.0MeV": "../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/RBS/"}

## Define the file endings for each beam energy that should be processed
sn116Files = {
    "Ebeam=3.2MeV": ["04", "05", "06", "07", "08"],
    "Ebeam=3.5MeV": ["03", "04"],
    "Ebeam=3.9MeV": ["03", "04", "05"],
    "Ebeam=4.3MeV": ["04", "05", "06", "07", "08", "09", "10"],
    "Ebeam=4.7MeV": ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"],
    "Ebeam=5.0MeV": ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"]}

## Dictionary to store merged yields for each beam energy
mergedYields = {}

## Loop over each activation energy
for beam_energy, path in Paths.items():

    print(f"\nProcessing files for {beam_energy}")

    ## Initialize array for merged yield
    mergedYield = [0 for i in range(512)]

    ## Get the relevant 116Sn activation run files for each beam energy
    valid_sufixes = sn116Files.get(beam_energy, [])

    ## Loop over the activation runs
    for file in sorted(os.listdir(path)):
        ## Check the file endings for the RBS runs
        if file.endswith(".SI2.dat"):
            ## Extract the run label (e.g., "2407084" from "2407084.SI2.dat")
            label = file.replace(".SI2.dat", "")
        ## Check if the last character matches the valid suffixes
        if label[-2:] in valid_sufixes:
            ## Read RBS data
            ch, y = ReadActivationRBS(os.path.join(path, file))
            mergedYield = [mergedYield[i] + y[i] for i in range(len(mergedYield))]
    ## Store the merged yield for this beam energy
    mergedYields[beam_energy] = mergedYield
    PlotRBS(ch, mergedYield, beam_energy)

## Plot merged RBS yields
labs = [f"{key}" for key in mergedYields.keys()]
#print(labs)
#Plot6RBS(ch, mergedYields, labs)
                
