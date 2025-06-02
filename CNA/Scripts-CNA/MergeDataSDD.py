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
        Path = str(Dir+file)
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
energies = [(c*0.031059-0.004137) for c in Channel] # keV
mergedYields = []
labels = []

for dir in SDD_Dir:

    Yield_SDD = MergeYield_MCA(dir)
    mergedYields.append(Yield_SDD)
    output_filename = str(dir[15:27]+"_"+os.listdir(dir)[0][0:18]+"_Merged.txt")
    labels.append(dir[15:27])
    """with open(output_filename, 'w') as outfile:
        for value in Yield_SDD:
            outfile.write(f"{value}\n")
    print(f"Output file: {output_filename}") """

    """     fig, ax = plt.subplots()
    ax.plot(energies, Yield_SDD,'+-', color ='xkcd:black', label=dir[15:27])
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy [keV]',fontsize=22)
    ylabel('Total Yield', fontsize=22)
    #xlim(0, 30)
    show() """

colors = ['xkcd:blue', 'xkcd:green', 'xkcd:orange', 'xkcd:red', 'xkcd:purple', 'xkcd:brown']
markers = ['1', '2', '3', '4', '8', 's']

fig, ax = plt.subplots()
ax.set_yscale('log')
for i, (Yield_SDD, dir) in enumerate(zip(mergedYields, SDD_Dir)):
    ax.plot(Channel, Yield_SDD, markers[i], color=colors[i], label=labels[i])
legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
ylabel('Total Yield', fontsize=22)
#xlim(0, 30)
show()