#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
##########################################
##########################################
def Plot(File):
    """
    Plots yield vs channel data from our .mca files
    INPUTS: "FileName.mca"
    OUTPUTS: yield vs channel plot
    """
    y, ch = Ge2Lists(File) 
    lab = str(File).replace('.TXT','')
    fig, ax = plt.subplots()
    ax.semilogy(ch,y,'.-', color ='xkcd:black', label=(str(lab)+' - Ge'))
    legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

#################
###   PLOTS   ###
#################

## Last runs
""" Plot('DataFilesGe/Decay/416040G2.TXT')
Plot('DataFilesGe/Decay/416041G2.TXT')
Plot('DataFilesGe/Decay/416042G2.TXT')
Plot('DataFilesGe/Decay/416043G2.TXT')
Plot('DataFilesGe/Decay/416044G2.TXT') """


## Calibration runs
path = '../Calibration/BEGe-Calib/Calib/'
for file in os.listdir(path):
    Plot(str(path+file))

## Decay runs
""" path = '../2_Decay/DataFilesGe/Decay/'
for file in os.listdir(path):
    Plot(str(path+file)) """