#RiP
####################################
from ReadData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import os
####################################

############################################################################
def MergeRateBgRmGe(path):
    """
    Merges rate from different data .TXT files from Ge detector, 
    in a specific directory, into a single list
    INPUTS:
    directory containing data files
    OUTPUTS:
    Merged yield list
    """
    ############################
    ## Calculation of bg rate ##
    ############################
    bgFile = '../Calibration/BEGe-Calib/Background/415114G2.TXT'
    bgYield = Ge2Lists(bgFile)[0] # counts
    bgSpan = 3849. # seconds = 64 min 9 sec
    bgRate = [counts/bgSpan for counts in bgYield]

    #######################################
    ## Remove bg rate for each decay run ##
    #######################################
    mergeYield = [0 for i in range(1024)]
    runSpan = 900 # sec = 15 minutes
    ## loop over decay runs
    for file in os.listdir(path):
        decayYield = Ge2Lists(str(path+file))[0]
        decayRate = [counts/runSpan for counts in decayYield]
        decayRateBgRm = [decay - bg for decay, bg in zip(decayRate, bgRate)]
        mergeYield = [mergeYield[i] + decayRateBgRm[i] for i in range(len(mergeYield))]
        
    return mergeYield

##################################
## Ge rate bg rm merge and plot ##
##################################
gePath = "../2_Decay/DataFilesGe/Decay/"
channel = [i+1 for i in range(1024)]
yieldGe = MergeRateBgRmGe(gePath)

fig, ax = plt.subplots()
ax.semilogy(channel, yieldGe,'+-', color ='xkcd:black', label=('Ge rate bg rm merged'))
legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
ylabel('Rate ($s^{-1}$)', fontsize=22)
show()