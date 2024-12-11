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
gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/',]

## Loop over different activation energies
""" for path in gePaths:
    
    Accu_Ka, Accu_Kb, Accu_g, Accu_t = AccumulateGe(path)

    ## Accumulation plot
    fig, ax = plt.subplots()
    ax.semilogy(Accu_t, Accu_g,'*-', color ='xkcd:red', label=('$\gamma$ - 158 keV'))
    ax.semilogy(Accu_t, Accu_Ka,'^-', color ='xkcd:blue', label=('Ka'))
    ax.semilogy(Accu_t, Accu_Kb,'.-', color ='xkcd:black', label=('Kb'))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (minutes)',fontsize=22)
    ylabel('Yield', fontsize=22)
    title(str(path[15:27]+' - '+path[-5:-1]))
    show() """


############################################################
## Calculate 117Sb half-life from decay accumulation data ##
############################################################

## For the 3.2 MeV run
file = gePaths[0]

## Exctract data from file
accu_Ka, accu_Kb, accu_gamma, accu_time = AccumulateGe(file)

## First calculate for the Ka yield
initParams = [3e5, 7e-5] ## N_Dirr ~ 3e5 counts, T1/2 ~ 1e4 seconds <=> lambda ~ 7e-5 sec^-1

## Fit the data
FitNdecay(Ndecay, accu_time, accu_Ka, initParams, lab=str(file[15:27]+' - '+file[-5:-1]), roid=0, roiu=300)