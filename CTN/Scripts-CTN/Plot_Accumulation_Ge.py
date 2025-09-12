#############################################
## Script to plot BEGe accumulation at CTN ##
#############################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Path for BEGe decay data files
gePath = '../2_Decay/DataFilesGe/BgRemoved/' 

## Define initial guess for N0 and bgRate
##                [[gamma]    , [ Ka  ]    , [ Kb  ]] 
initParamsNpeak = [[9.0e5, 10.], [8.0e5, 1.], [2.0e5, 1.]]

## Convoluted efficiencies nominal value  and uncertainty
efficiency_params = [[6.996e-2, 2.53e-3], [7.474e-2, 2.64e-3], [1.656e-2, 5.6e-4]]

## Transportation time
t_transMin = 23. #minutes

radType = ["gamma", "Ka", "Kb"]

## Extract data from files
accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_gamma, accu_gamma_err, accu511, accu_time = AccumulateGe_BgRemove(gePath)

## Fit the data for Npeak
FitNpeakBEGe(Npeak, accu_time, accu_gamma, accu_gamma_err, 
                    accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, 
                    initParamsNpeak, efficiency=efficiency_params, t_trans=t_transMin,
                    radtype=radType, lab=str('Ebeam = 3.2 MeV - BEGe @ CTN'))