#RiP

from ReadData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import os

##############################################################################################
def MergeYield_MCA(Dir):
    """
    Merges yields from different data .mca files, in a specific directory, into a single list
    INPUTS:
    directory containing data files
    OUTPUTS:
    Merged yield list
    """
    ConvYield = [0 for i in range(2048)]
    for file in os.listdir(Dir):
        Path = str(Dir+"\\"+file)
        Yield = MCA2Lists(Path)[0]
        ConvYield = [ConvYield[i] + Yield[i] for i in range(len(ConvYield))]
    return ConvYield


###   SDD Acquisition merge and plot   ###
SDD_Dir = "DataFilesSDD/Decay"
Channel = [i+1 for i in range(2048)]
Yield_SDD = MergeYield_MCA(SDD_Dir)

fig, ax = plt.subplots()
ax.plot(Channel, Yield_SDD,'+-', color ='xkcd:black', label=('SDD'))
legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
ylabel('Yield', fontsize=22)
#grid()
show()
###########################################