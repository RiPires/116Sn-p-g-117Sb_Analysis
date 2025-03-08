#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
##########################################
##########################################
def PlotBgRemoved(File):
    """
    Plots yield vs channel data from our .mca files
    INPUTS: "FileName.mca"
    OUTPUTS: yield vs channel plot
    """
    y, ch = Ge2ListsBgRm(File)
    lab = str(File).replace('.TXT','').replace('DataFiles_HPGe/20240708/','')
    fig, ax = plt.subplots()
    ax.semilogy(ch,y,'.-', color ='xkcd:black', label=(str(lab)))
    legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

#################
###   PLOTS   ###
#################

## Decay runs
path = '../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved/HPGe/'
for file in sorted(os.listdir(path)):
    PlotBgRemoved(str(path+file))