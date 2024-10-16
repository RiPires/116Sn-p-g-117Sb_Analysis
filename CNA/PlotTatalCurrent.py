######################################################
## Script to plot total current for each activation ##
######################################################

## -------------------- ##
from PlotData import *
from ReadData import *
## -------------------- ##

## Paths for each activation energy
iPath32 = 'Ebeam=3.2MeV/1_Irradiation/DataFiles/240708/Counter/'
iPath35 = 'Ebeam=3.5MeV/1_Irradiation/DataFiles/240709/Counter/'
iPath39 = 'Ebeam=3.9MeV/1_Irradiation/DataFiles/240710/Counter/'
iPath43 = 'Ebeam=4.3MeV/1_Irradiation/DataFiles/240711/Counter/'
iPath47 = 'Ebeam=4.7MeV/1_Irradiation/DataFiles/240712/Counter/'
iPath50 = 'Ebeam=5.0MeV/1_Irradiation/DataFiles/240715/Counter/'

## time and current lists
time32, current32 = ReadCurrent(iPath32)
time35, current35 = ReadCurrent(iPath35)
time39, current39 = ReadCurrent(iPath39)
time43, current43 = ReadCurrent(iPath43)
time47, current47 = ReadCurrent(iPath47)
time50, current50 = ReadCurrent(iPath50)

## Plot for each activatino
PlotI(time32, current32, iPath32[0:12])
PlotI(time35, current35, iPath35[0:12])
PlotI(time39, current39, iPath39[0:12])
PlotI(time43, current43, iPath43[0:12])
PlotI(time47, current47, iPath47[0:12])
PlotI(time50, current50, iPath50[0:12])
