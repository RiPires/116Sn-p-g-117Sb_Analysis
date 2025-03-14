#################### RiP #########################
## Script for plotting detector background runs ##
##################################################

## ---------------------------- ##
from include.ReadData import*
from include.PlotData import *
## ---------------------------- ##


## Background before the decay
bgFile = '../Calibration/BEGe-Calib/Background/415114G2.TXT'
ch_hpge = [(i+1) for i in range(1024)]
bg_yield = Ge2Lists(bgFile)[0]
Plot(ch_hpge, bg_yield, 'BEGe background')