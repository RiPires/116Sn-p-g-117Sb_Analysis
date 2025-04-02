#######################################################
## Script to integrate the Sn RBS peak for every run ##
## during the activation                             ##
#######################################################

## ------------------------------------------- ##
import os
from include.ReadData import ReadActivationRBS  
from include.PlotData import PlotRBS
## ------------------------------------------- ##

## Path for the RBS files during irradiation
rbsPath = "../1_Irradiation/DataFiles/Activation/RBS/"

## Lower and Upper Region of Interest limits
rois = [505, 535]

## Initialize total integral
peakIntegral = 0.

## Loop over each run
for file in sorted(os.listdir(rbsPath)):
    
    print(f"Processing file: {file}")
    ## Extract the run label
    label = file.replace("Activation_","").replace(".mpa","")

    ## Read the run data
    ch, rbsYield = ReadActivationRBS(rbsPath+file, 4)
    #PlotRBS(ch, rbsYield, label)

    ## Perform Sn peak yield integration (sum of the yields channel by channel)
    integralValue = sum([counts for counts in rbsYield[rois[0]:rois[1]]])
    peakIntegral += integralValue

    ## Print the integration result
    print(f"Run integral: {integralValue:.2e} \n")

print(f"Np = {peakIntegral:.2e}")
