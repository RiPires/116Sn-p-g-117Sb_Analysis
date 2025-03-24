#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
import random
import itertools
##########################################
##########################################

##########################################
##########################################
def PlotAll():

    ch = [(i+1) for i in range(2048)]
    path = '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved_LiveTime/'
    
    nr_colors = len(os.listdir(path))
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(nr_colors)]
    markers = itertools.cycle((".", ",", "o", "v", "^", "<", ">", "1", "2", 
               "3", "4", "8", "s", "p", "*", "h", "+","x", "d"))
    counter = 0

    fig, ax= plt.subplots()
    #ax.set_yscale("log")
    for file in sorted(os.listdir(path)):
        y = MCA2ListsBgRm(path+file)[0]
        ax.plot(ch, y, linestyle=":", marker=next(markers), color =colors[counter], label=file.replace(".mca","").replace("116Sn-C3_Decay_SDD","Run"))
        counter+=1
    #legend = ax.legend(loc="upper right",ncol=3, shadow=False,fancybox=True,framealpha = 0.0,fontsize=10)
    #legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=20)
    xlabel("Channel", fontsize=20)
    ylabel("Yield", fontsize=20)

    show()

    return

## Plot
PlotAll()