############################################
## Script to plot SDD accumulation at CTN ##
############################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for SDD decay data files
sddPath = "../2_Decay/DataFilesSDD/Decay/"
## Define initial guess N_Dirr and bgRate for each beam energy
##           [[Ka]       , [Kb]] 
initParams = [[1.0e6, 1.], [2.5e5, 1.]]  # Example values for 3.2 MeV

## Extract data from files
accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_time = AccumulateSDD(sddPath)

## Fit the data for Npeak
FitNpeakSDD(NpeakSDD,   accu_time, accu_Ka, accu_Ka_err, 
                        accu_Kb, accu_Kb_err, initParams, 
                        lab=str(sddPath[15:27]+' - '+sddPath[-5:-1]))