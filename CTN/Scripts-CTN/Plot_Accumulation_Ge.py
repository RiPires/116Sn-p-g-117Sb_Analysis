############################################################
## Script to plot BEGe accumulation at different energies ##
############################################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Path for BEGe decay data files
gePath = '../2_Decay/DataFilesGe/BgRemoved/' 

## Define initial guess N_Dirr and BgRate for each beam energy
##                [[gamma]    , [ Ka  ]    , [ Kb  ]] 
initParamsNpeak = [[9.0e5, 1.], [8.0e5, 1.], [2.0e5, 1.]] # Example values for 3.2 MeV

## Extract data from files
accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, accu_gamma, accu_gamma_err, accu511, accu_time = AccumulateGe_BgRemove(gePath)

## Fit the data for Npeak
FitNpeakBEGe(NpeakBEGe, accu_time, accu_gamma, accu_gamma_err, 
                        accu_Ka, accu_Ka_err, accu_Kb, accu_Kb_err, 
                        initParamsNpeak, lab=str(gePath[15:27]+' - '+gePath[-5:-1]))