###########################################################
## Script to plot SDD accumulation at different energies ##
###########################################################

## -------------------------- ##
import os
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from Accumulation import *
## -------------------------- ##

## Paths for different energy decays
sddPaths = ['Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
           'Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
           'Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
           'Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
           'Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
           'Ebeam=5.0MeV/2_Decay/DataFiles_SDD/',]

## Loop over different activation energies
for path in sddPaths:
    
    Accu_Ka, Accu_Kb, Accu_t = AccumulateSDD(path)

    ## Accumulation plot
    fig, ax = plt.subplots()
    ax.plot(Accu_t, Accu_Ka,'^-', color ='xkcd:blue', label=('Ka'))
    ax.plot(Accu_t, Accu_Kb,'.-', color ='xkcd:black', label=('Kb'))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (minutes)',fontsize=22)
    ylabel('Yield', fontsize=22)
    title(str(path[0:12]+' - '+path[-4:-1]))    
    show()