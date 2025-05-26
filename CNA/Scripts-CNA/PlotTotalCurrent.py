######################################################
## Script to plot total current for each activation ##
######################################################

## -------------------------- ##
from include.PlotData import *
from include.ReadData import *
## -------------------------- ##

## Paths for each activation energy
iPath32 = '../Activations/Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/Counter/'
iPath35 = '../Activations/Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/Counter/'
iPath39 = '../Activations/Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/Counter/'
iPath43 = '../Activations/Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/Counter/'
iPath47 = '../Activations/Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/Counter/'
iPath50 = '../Activations/Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/Counter/'

## time and current lists
time32, current32 = ReadCurrent(iPath32)
time35, current35 = ReadCurrent(iPath35)
time39, current39 = ReadCurrent(iPath39)
time43, current43 = ReadCurrent(iPath43)
time47, current47 = ReadCurrent(iPath47)
time50, current50 = ReadCurrent(iPath50)

times = [time32, time35, time39, time43, time47, time50]
currents = [current32, current35, current39, current43, current47, current50]
labs = [iPath32[15:27], iPath35[15:27], iPath39[15:27], iPath43[15:27],iPath47[15:27], iPath50[15:27]]

## Plot for each activation
""" PlotI(time32, current32, iPath32[15:27])
PlotI(time35, current35, iPath35[15:27])
PlotI(time39, current39, iPath39[15:27])
PlotI(time43, current43, iPath43[15:27])
PlotI(time47, current47, iPath47[15:27])
PlotI(time50, current50, iPath50[15:27]) """

## Plot all activations in same frame
Plot6I(times, currents, labs)
