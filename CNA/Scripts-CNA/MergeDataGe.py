#RiP
####################################
from include.ReadData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import os
####################################

############################################################################
def MergeYieldGe(Dir):
    """
    Merges yields from different data .TXT files from Ge detector, 
    in a specific directory, into a single list
    INPUTS:
    directory containing data files
    OUTPUTS:
    Merged yield list
    """
    ConvYield = [0 for i in range(4096)]
    for file in os.listdir(Dir):
        Path = str(Dir+"\\"+file)
        Yield = Ge2ListsBgRm(Path)[0]
        ConvYield = [ConvYield[i] + Yield[i] for i in range(len(ConvYield))]
    return ConvYield

#########################################
###   Ge Acquisition merge and plot   ###
#########################################
geDir = "../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved/HPGe/"
Channel = [(i+1) for i in range(4096)]
Yield_Ge = MergeYieldGe(geDir)

### Plot
fig, ax = plt.subplots()
ax.semilogy(Channel, Yield_Ge,'+-', color ='xkcd:black', label=('HPGe - Ebeam = 3.5 MeV'))
legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
xlim(left=0.)
ylabel('Total yield', fontsize=22)
show()
###########################################