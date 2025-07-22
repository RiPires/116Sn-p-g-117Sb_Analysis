############### RiP ##################
## Plot every Ge run of a specific  ##
## activation in the same axes      ##
######################################

## ----------------------------- ##
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
import random
import itertools
## ----------------------------- ##

##########################################
##########################################
def PlotSome():

    ch = [(i+1) for i in range(4096)]
    path = '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/'
    
    nr_colors = len(os.listdir(path))
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(nr_colors)]
    markers = itertools.cycle(("1", "2", "3",".", ",", "o", "v", "^", "<", ">", "1", "2", 
               "3", "4", "8", "s", "p", "*", "h", "+","x", "d"))
    counter = 0

    fig, ax= plt.subplots()
    #ax.set_yscale("log")
    for file in list(sorted(os.listdir(path))[i] for i in [0, 20, 50, 100]):
        y = Ge2Lists(path+file)[0]
        ax.semilogy(ch, y, linestyle=":", marker=next(markers), color =colors[counter], markersize=10, label=file.replace(".mca","").replace("116Sn-C3_Decay_SDD","Run"))
        counter+=1
    legend = ax.legend(loc="upper right",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=18)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=20)
    xlabel("Channel", fontsize=20)
    ylabel("Yield", fontsize=20)

    show()

    return

##########################################
##########################################
def PlotAll():

    ch = [(i+1) for i in range(4096)]
    path = '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/'
    
    nr_colors = len(os.listdir(path))
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(nr_colors)]
    markers = itertools.cycle(("1", "2", "3",".", ",", "o", "v", "^", "<", ">", "1", "2", 
               "3", "4", "8", "s", "p", "*", "h", "+","x", "d"))
    counter = 0

    fig, ax= plt.subplots()
    #ax.set_yscale("log")
    for file in list(sorted(os.listdir(path))):
        y = Ge2Lists(path+file)[0]
        ax.semilogy(ch, y, linestyle=":", marker=next(markers), color =colors[counter], label=file.replace(".mca","").replace("116Sn-C3_Decay_SDD","Run"))
        counter+=1
    #legend = ax.legend(loc="upper right",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=10)
    #legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=20)
    xlabel("Channel", fontsize=20)
    ylabel("Yield", fontsize=20)
    title(path[15:27], fontsize=20)
    show()

    return

## Plot
PlotSome()