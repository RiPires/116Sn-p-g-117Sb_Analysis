#######################################################
## Script to integrate the Sn RBS peak for every run ##
## during the activation                             ##
#######################################################

## ------------------------------------------- ##
import os
from include.ReadData import ReadActivationRBS  
from include.PlotData import PlotRBS
import numpy as np
from include.Merge import Merge
## ------------------------------------------- ##

## Path for the RBS files during irradiation
rbsPath = "../1_Irradiation/DataFiles/Activation/RBS/"

## Lower and Upper Region of Interest limits
rois = [510, 530]

## Initialize total integral
peakIntegral = 0.
integratedYield = np.array([])

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
    print(f"Run integral: {integralValue:.3e} \n")


print(f"Np = {peakIntegral:.3e}")

## Merge online Ge data
mergedGeYield = Merge("../2_Decay/DataFilesGe/Decay/", "onlineGe")
channel = [i+1 for i in range(8192)]
PlotRBS(channel, mergedGeYield, "Merged online Ge data")
