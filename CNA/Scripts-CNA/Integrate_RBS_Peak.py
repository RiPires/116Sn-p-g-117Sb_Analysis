#######################################################
## Script to integrate the Sn RBS peak for every run ##
## of each beam energy                               ##
#######################################################

## ------------------------------------------- ##
import os
from include.ReadData import ReadActivationRBS  
## ------------------------------------------- ##

# Define paths for different beam energies
Paths = {
"Ebeam=3.2MeV": "../Activations/Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/RBS/",
"Ebeam=3.5MeV": "../Activations/Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/RBS/",
"Ebeam=3.9MeV": "../Activations/Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/RBS/",
"Ebeam=4.3MeV": "../Activations/Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/RBS/",
"Ebeam=4.7MeV": "../Activations/Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/RBS/",
"Ebeam=5.0MeV": "../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/RBS/",
}

# Define the file endings for each beam energy that should be processed
# the ones that correspond to the  activation runs
sn116Files = {
"Ebeam=3.2MeV": ["04", "05", "06", "07", "08"],
"Ebeam=3.5MeV": ["03", "04"],
"Ebeam=3.9MeV": ["03", "04", "05"],
"Ebeam=4.3MeV": ["04", "05", "06", "07", "08", "09", "10"],
"Ebeam=4.7MeV": ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"],
"Ebeam=5.0MeV": ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"],
}

# Define the Region Of Interest lower and upper bounds for the Sn RBS peak
# at each beam energy
rois = {"Ebeam=3.2MeV": [412, 440],
        "Ebeam=3.5MeV": [454, 485],  
        "Ebeam=3.9MeV": [393, 417],
        "Ebeam=4.3MeV": [436, 461],
        "Ebeam=4.7MeV": [407, 448],
        "Ebeam=5.0MeV": [434, 476],}

# Loop over the activation energies
for beam_energy, path in Paths.items():
    print(f"\nProcessing files for {beam_energy}")

    ## Initialize total integral
    peakIntegral = 0.

    # Get the relevant 116Sn activation run files
    valid_suffixes = sn116Files.get(beam_energy, [])

    ## Get the ROI limits
    valid_rois = rois.get(beam_energy, [])

    ## Loop over the activation runs
    for file in sorted(os.listdir(path)):
        ## Checks it is a RBS file
        if file.endswith(".SI2.dat"):
            # Extract the run label (e.g., "2407084" from "2407084.SI2.dat")
            label = file.replace(".SI2.dat", "")

            ## Check if the last characters match the valid suffixes
            if label[-2:] in valid_suffixes:

                ## Read data
                ch, y = ReadActivationRBS(os.path.join(path, file))

                ## Define ROI lower and upper bounds
                roiLow = valid_rois[0]
                roiUp = valid_rois[1]

                ## Perform the peak integration (sum the yield values inside ROI)
                integral_value = sum([counts for counts in y[roiLow:roiUp]])
                
                ## Adds the integral of this run to the total activation integral
                peakIntegral +=integral_value

                ## Format the output label
                lab = f"Run {label}"

                # Print the integration result for this run
                print(f"{lab}: {integral_value:.2e}")
    
    ## Print the total activation integral for this beam energy, Np 
    print(f"\n Np = {peakIntegral:.2e}")