###########################################################
## Script to plot SDD accumulation at different energies ##
###########################################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different energy decays
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/',]

############################################################
## Calculate 117Sb half-life from decay accumulation data ##
############################################################
## Loop over different activation energies
for file in sddPaths:
    
    ## Exctract data from file
    accu_Ka, accu_Kb, accu_t = AccumulateSDD(file)

    ## Accumulation plot
    """fig, ax = plt.subplots()
    ax.semilogy(accu_t, accu_Ka,'^-', color ='xkcd:blue', label=('Ka'))
    ax.semilogy(accu_t, accu_Kb,'.-', color ='xkcd:black', label=('Kb'))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (minutes)',fontsize=22)
    ylabel('Yield', fontsize=22)
    title(str(file[15:27]+' - '+file[-4:-1]), fontsize=24)    
    show() """

    ## Initial guesses for fit parameters [[gamma], [Ka], [Kb]]
    initParams = [[5e3, 7e-5], [5e2, 7e-5]] ## N_Dirr ~ 3e5 counts, T1/2 ~ 1e4 seconds <=> lambda ~ 7e-5 sec^-1

    ## Fit the data
    FitNdecaySDD(Ndecay, accu_t, accu_Ka, accu_Kb, initParams, lab=str(file[15:27]+' - '+file[-4:-1]))