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
    
    Data1_x, Data1_y = Read_TANDEM_RBS_Data(data, 1) ## Detector MOV E
    Data3_x, Data3_y = Read_TANDEM_RBS_Data(data, 3) ## Detector MOV D
    

    Label = Label.replace('.mpa', '')
    fig, ax = plt.subplots()
    ax.semilogy(Data1_x,Data1_y,'.-', color ='xkcd:black', label=str(Label+' - MOV E'))
    ax.semilogy(Data3_x,Data3_y,'.-', color ='xkcd:blue', label=str(Label+' - MOV D'))
    legend = ax.legend(loc="upper left",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Counts', fontsize=22)
    show()

    return
##################################################
##################################################


#################
###   PLOTS   ###
#################

## Triple alpha source runs
path = '../1_Irradiation/DataFiles/Calib_3-alfa/'
for file in os.listdir(path):
    PlotData(str(path+file), str(file))

""" 
## Sn and Formvar + Al runs
path = '../1_Irradiation/DataFiles/Sn&Formvar+Al/'
for file in os.listdir(path):
    PlotData(str(path+file), str(file)) """