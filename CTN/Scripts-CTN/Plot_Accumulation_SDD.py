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

## Define initial guess of N0 and bgRate
##           [[Ka      ], [Kb      ]] 
initParams = [[1.0e6, 1], [1.0e6, 1]]

## Convoluted efficiencies
## Parameters for the detector at mean position of (9+7)/2 mm
##                  [[Ka            ], [Kb            ]] 
efficiency_params = [[1.865e-3, 5e-4], [2.472e-4, 6e-5]]

## Transportation time
t_transMin = 15. # minutes

radType = ["Ka", "Kb"]

## Extract data from files
accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_time = AccumulateSDD(sddPath)

## Fit the data for Npeak
FitNpeakSDD(Npeak,  accu_time, accu_Ka, accu_Ka_err, 
                    accu_Kb, accu_Kb_err, initParams,
                    efficiency=efficiency_params, t_trans=t_transMin,
                    lab=str('Ebeam=3.2MeV - SDD @ CTN'))