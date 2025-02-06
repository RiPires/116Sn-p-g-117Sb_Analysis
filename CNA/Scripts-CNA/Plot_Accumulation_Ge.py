############################################################
## Script to plot HPGe accumulation at different energies ##
############################################################

## -------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from include.Accumulation import *
from include.Fits import *
## -------------------------- ##

## Paths for different energy decays
gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved/HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved/HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved/HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved/HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved/HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved/HPGe/',]

############################################################
## Calculate 117Sb half-life from decay accumulation data ##
############################################################

## Loop over different activation energies
for files in gePaths:
    
    ## Exctract data from file
    accu_Ka, accu_Kb, accu_gamma, accu511, accu_time = AccumulateGe_BgRemove(files)

    ## Accumulation plot
    """fig, ax = plt.subplots()
    ax.semilogy(accu_time, accu_gamma,'*-', color ='xkcd:red', label=('$\gamma$ - 158 keV'))
    ax.semilogy(accu_time, accu_Ka,'^-', color ='xkcd:blue', label=('Ka'))
    ax.semilogy(accu_time, accu_Kb,'.-', color ='xkcd:black', label=('Kb'))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (minutes)',fontsize=22)
    ylabel('Yield', fontsize=22)
    title(str(file[15:27]+' - '+file[-5:-1]))
    show()  """

    ## Initial guesses for Npeak fit parameters
    ##                  Ndirr, eta, epsilonD
    initParamsNpeak = [[1.2e6, 1.0, 0.0101], # gamma
                       [1.2e6, 1.0, 0.0718], # Ka
                       [2.8e5, 0.2, 0.0629]] # Kb

    ## Fit the data for Npeak
    FitNpeakHPGe(Npeak, accu_time, accu_gamma, accu_Ka, accu_Kb, initParamsNpeak, lab=str(files[15:27]+' - '+files[-5:-1]))