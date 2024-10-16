#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
from ReadData import*
##########################################

##########################################
def PlotBgGe(File):
    """
    Plots yield vs channel data from our .mca files
    INPUTS: "FileName.mca"
    OUTPUTS: yield vs channel plot
    """
    y, ch = Ge2Lists(File) 
    lab = str(File).replace('.TXT','')
    fig, ax = plt.subplots()
    ax.plot(ch,y,'.-', color ='xkcd:black', label=(str(lab)+' - Ge'))
    legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

    return
###############################################

#############################
## Plot raw background run ##
#############################
bgFile = 'DataFilesGe/Background/415114G2.TXT'
PlotBgGe(bgFile)