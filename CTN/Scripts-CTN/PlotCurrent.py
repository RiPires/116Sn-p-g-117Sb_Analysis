################################################
## Script to plot current over the activation ##
################################################

## --------------------------- ##
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import csv
from include.ReadData import *
from include.PlotData import *
## --------------------------- ##

iFile = '../1_Irradiation/DataFiles/Sn116-pg-240516_CurrentMonitor.dat'

time, current = ReadCurrent(iFile)

PlotI(time, current, 'Current')

