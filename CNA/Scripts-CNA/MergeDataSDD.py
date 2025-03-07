#RiP

from include.ReadData import *
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
SDD_Dir = ["../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_SDD/",
           "../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_SDD/",
           "../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_SDD/",
           "../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_SDD/",
           "../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_SDD/",
           "../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/"]

Channel = [i+1 for i in range(2048)]

for dir in SDD_Dir:

    Yield_SDD = MergeYield_MCA(dir)
    output_filename = str(dir[15:27]+"_"+os.listdir(dir)[0][0:18]+"_Merged.txt")
    with open(output_filename, 'w') as outfile:
        for value in Yield_SDD:
            outfile.write(f"{value}\n")
    print(f"Output file: {output_filename}")

    fig, ax = plt.subplots()
    ax.plot(Channel, Yield_SDD,'+-', color ='xkcd:black', label=(output_filename))
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Total Yield', fontsize=22)
    xlim(0, 1000)
    show()
    ###########################################