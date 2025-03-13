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
        Path = str(Dir+file)
        Yield = Ge2ListsBgRm(Path)[0]
        ConvYield = [ConvYield[i] + Yield[i] for i in range(len(ConvYield))]
    return ConvYield

#########################################
###   Ge Acquisition merge and plot   ###
#########################################
geDir = ["../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_BgRemoved/HPGe/",
         "../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_BgRemoved/HPGe/",
         "../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_BgRemoved/HPGe/",
         "../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_BgRemoved/HPGe/",
         "../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_BgRemoved/HPGe/",
         "../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_BgRemoved/HPGe/"]


Channel = [(i+1) for i in range(4096)]
for dir in geDir:

    Yield_Ge = MergeYieldGe(dir)
    output_filename = str(dir[15:27]+"_"+os.listdir(dir)[0][0:19]+"_BgRemoved_Merged.txt")
    with open(output_filename, 'w') as outfile:
        for value in Yield_Ge:
            outfile.write(f"{value}\n")
    print(f"Output file: {output_filename}")


    ### Plot
    fig, ax = plt.subplots()
    ax.semilogy(Channel, Yield_Ge,'+-', color ='xkcd:black', label=(output_filename))
    legend = ax.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    xlim(left=0.)
    ylabel('Total yield', fontsize=22)
    show()
    ###########################################