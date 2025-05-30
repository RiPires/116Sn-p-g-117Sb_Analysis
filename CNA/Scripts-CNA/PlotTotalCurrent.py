######################################################
## Script to plot total current for each activation ##
######################################################

## -------------------------- ##
from include.PlotData import *
from include.ReadData import *
import numpy as np
## -------------------------- ##

## Paths for each activation energy
iPath32 = '../Activations/Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/Counter/'
iPath35 = '../Activations/Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/Counter/'
iPath39 = '../Activations/Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/Counter/'
iPath43 = '../Activations/Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/Counter/'
iPath47 = '../Activations/Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/Counter/'
iPath50 = '../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/Counter/'

## Irradiation start time for each activation
irradStart32 = '11:30:07'
irradStart35 = '10:40:00'
irradStart39 = '10:42:50'
irradStart43 = '10:25:44'
irradStart47 = '10:33:18'
irradStart50 = '10:37:00'

## Irradiation end time for each activation
irradEnd32 = '17:28:00'
irradEnd35 = '16:45:00'
irradEnd39 = '16:43:00'
irradEnd43 = '16:27:00'
irradEnd47 = '16:20:00'
irradEnd50 = '16:21:00' 

## Time and current lists during the activation  
time32, current32 = ReadCurrentActivation(iPath32, irradStart32, irradEnd32)
time35, current35 = ReadCurrentActivation(iPath35, irradStart35, irradEnd35)
time39, current39 = ReadCurrentActivation(iPath39, irradStart39, irradEnd39)
time43, current43 = ReadCurrentActivation(iPath43, irradStart43, irradEnd43)
time47, current47 = ReadCurrentActivation(iPath47, irradStart47, irradEnd47)
time50, current50 = ReadCurrentActivation(iPath50, irradStart50, irradEnd50)

times = [time32, time35, time39, time43, time47, time50]
currents = [current32, current35, current39, current43, current47, current50]
labs = [iPath32[15:27], iPath35[15:27], iPath39[15:27], iPath43[15:27],iPath47[15:27], iPath50[15:27]]

print(np.sum(current32))

## Calculate mean current during the activation, for each beam energy
averageI32 = np.sum(current32) / len(current32)
stdI32 = (sum((x - averageI32) ** 2 for x in current32) / len(current32)) ** 0.5
averageI35 = sum(current35) / len(current35)
stdI35 = (sum((x - averageI35) ** 2 for x in current35) / len(current35)) ** 0.5
averageI39 = sum(current39) / len(current39)
std39 = (sum((x - averageI39) ** 2 for x in current39) / len(current39)) ** 0.5
averageI43 = sum(current43) / len(current43)
std43 = (sum((x - averageI43) ** 2 for x in current43) / len(current43)) ** 0.5
averageI47 = sum(current47) / len(current47)
std47 = (sum((x - averageI47) ** 2 for x in current47) / len(current47)) ** 0.5
averageI50 = sum(current50) / len(current50)
std50 = (sum((x - averageI50) ** 2 for x in current50) / len(current50)) ** 0.5

averageIs = [averageI32, averageI35, averageI39, averageI43, averageI47, averageI50]
stds = [stdI32, stdI35, std39, std43, std47, std50]
for i, current in enumerate(averageIs):
    print(f'Average current for {labs[i]} = ({current:.2f} +- {stds[i]:.2f}) nA')

## Plot for each activation
""" PlotI(time32, current32, iPath32[15:27])
PlotI(time35, current35, iPath35[15:27])
PlotI(time39, current39, iPath39[15:27])
PlotI(time43, current43, iPath43[15:27])
PlotI(time47, current47, iPath47[15:27])
PlotI(time50, current50, iPath50[15:27])
 """

## Plot all activations in same canva
Plot6I(times, currents, labs)
