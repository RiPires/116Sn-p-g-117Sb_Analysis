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

## Define SimNRA simulation files
simnraFiles = {
    "Ebeam=3.2MeV": "Analysis-RBS_Ebeam3200keV.txt",
    "Ebeam=3.5MeV": "Analysis-RBS_Ebeam3500keV.txt",
    "Ebeam=3.9MeV": "Analysis-RBS_Ebeam3900keV.txt",
    "Ebeam=4.3MeV": "Analysis-RBS_Ebeam4300keV.txt",
    "Ebeam=4.7MeV": "Analysis-RBS_Ebeam4700keV.txt",
    "Ebeam=5.0MeV": "Analysis-RBS_Ebeam5000keV.txt"}

## Define both Exp. and Sim. calibration aprameters for each bema energy
calibParams = {   #         Exp.              Sim.
    "Ebeam=3.2MeV": [[6.6688, 204.837], [6.7476, 168.952]],
    "Ebeam=3.5MeV": [[6.7252, 174.977], [6.7226, 175.544]],
    "Ebeam=3.9MeV": [[8.6164, 240.163], [8.6218, 231.883]],
    "Ebeam=4.3MeV": [[8.7203, 200.564], [8.6510, 227.116]],
    "Ebeam=4.7MeV": [[10.028, 215.994], [9.8864, 262.641]],
    "Ebeam=5.0MeV": [[9.8013, 294.517], [9.9500, 235.000]]}

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
    #PlotRBS(ch, mergedYield, beam_energy)

    """     ## Opens file to write out merged RBS yield
    with open(f"RBS_{beam_energy}_Merged.dat", 'w') as outFile:
        for i in range(len(mergedYield)):
            outFile.write(f"{i+1}\t{mergedYield[i]:.0f}\n")
    outFile.close() """

    ## Reads SimNRA file
    ySim, chSim = ReadSimNRA(path.replace(path[-21:],'')+simnraFiles.get(beam_energy))

    ## Performs energy calibration and plots both exp and sim spectra
    eExp = [(c * calibParams[beam_energy][0][0] + calibParams[beam_energy][0][1]) for c in ch]
    eSim = [(ch * calibParams[beam_energy][1][0] + calibParams[beam_energy][1][1]) for ch in chSim]
    PlotRBSSim(eExp, mergedYield, eSim, ySim, beam_energy)

## Plot merged RBS yields
#labs = [f"{key}" for key in mergedYields.keys()]
#print(labs)
#Plot6RBS(ch, mergedYields, labs)
                
