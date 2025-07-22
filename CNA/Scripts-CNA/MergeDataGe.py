#RiP
####################################
from include.ReadData import *
from include.Merge import *
from include.PlotData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
import os
import numpy as np
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


Channel = np.array([(i+1) for i in range(4096)])
energy = Channel*0.3225 - 0.4556 # keV
mergedYields = []
labels = []
for dir in geDir:

    Yield_Ge = MergeYieldGe(dir)
    mergedYields.append(Yield_Ge)
    output_filename = str(dir[15:27]+"_"+os.listdir(dir)[0][0:19]+"_BgRemoved_Merged.txt")
    labels.append(output_filename[:5] + ' = ' + output_filename[6:9] + ' MeV - HPGe')
    """with open(output_filename, 'w') as outfile:
        for value in Yield_Ge:
            outfile.write(f"{value}\n")
    print(f"Output file: {output_filename}") """

    ## Check background
    ## Background runs path
    bgPath = '../Calibrations/HPGe/Background/'
    ## Get background merged yield and time
    mergeBgYield, _ = Merge(bgPath, 'ge')
    bgTime = 35*1800 + 777 ## seconds: 35 runs of 30 minutes each + 777 seconds for the last run

    ## Converts run yield into count rate (in s^-1)
    nrRuns = len(os.listdir(dir))
    acquiTime = 15 * 60 * nrRuns # seconds = 15 minutes
    runRate = [Yield_Ge[i]/acquiTime for i in range(len(Yield_Ge))]
    ## Converts background yield into background count rate (in s^-1)
    bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]
    ## Remove background rate from run data 
    runRateBgRem = [(runRate[i] - bgRate[i]) for i in range(len(runRate))]

    ## Set labels
    lab = dir[21:24] + ' MeV'
    bgLab = 'Background Rate'
    rateLab = lab +'_BG removed'

    ## Plot both run data, bg rate and run data with bg removed 
    Plot3RateLogy(Channel, runRate, bgRate, runRateBgRem, lab, bgLab, rateLab)


    """     ### Plot
    fig, ax1 = plt.subplots()
    ax1.semilogy(Channel, Yield_Ge,'+-', color ='xkcd:black', label=(output_filename[:5]+' =  '+
                                                                     output_filename[6:9]+' MeV - HPGe'))
    legend = ax1.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy (keV)',fontsize=22)
    xlim(left=0.)
    ylabel('Merged yield', fontsize=22)
    show() """

colors = ["xkcd:blue", "xkcd:green", "xkcd:orange", "xkcd:red", "xkcd:purple", "xkcd:brown"]
markers = ['1', '2', '3', '4', '8', 's']
fig, ax1 = plt.subplots()
for i, Yield_Ge in enumerate(mergedYields):
    ax1.semilogy(Channel, Yield_Ge, markers[i]+'-', color=colors[i], label=labels[i])
legend = ax1.legend(loc="best",ncol=2, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
xlim(left=0.)
ylabel('Merged yield', fontsize=22)
show()