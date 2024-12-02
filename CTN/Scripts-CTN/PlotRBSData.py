#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import csv
import os
from ReadRBSData import*
##########################################
##########################################
def PlotData(File, Label):

    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    
    Data1_x, Data1_y = ReadActivationRBS(data, 1) ## Detector MOV E
    Data3_x, Data3_y = ReadActivationRBS(data, 4) ## Detector MOV D
    
    fig, ax = plt.subplots()
    #ax.semilogy(Data1_x,Data1_y,'.',markersize=10, color ='xkcd:black', label=str(Label+' - MOV E'))
    ax.semilogy(Data3_x,Data3_y,'.-', markersize=10, color ='xkcd:magenta', label=str('Online RBS @ 155$^{\\circ}$'))
    ax.vlines(x=530, ymin=2e3, ymax=2e5, colors='red', ls='--', lw=2, label='Sn')
    ax.vlines(x=465, ymin=2e3, ymax=2e4, colors='green', ls=':', lw=2, label='Al')
    ax.vlines(x=420, ymin=2e3, ymax=2e4, colors='blue', ls='-.', lw=2, label='O')
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    xlim(350, 550)
    ylabel('Yield', fontsize=22)
    ylim(bottom=2e3)
    show()

    return


#################
###   PLOTS   ###
#################

## RBS during activation
path = '../1_Irradiation/DataFiles/Activation/'
for file in os.listdir(path):
    PlotData(str(path+file), str(file).replace('.mpa',''))