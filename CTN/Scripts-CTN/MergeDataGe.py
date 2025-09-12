###############  RiP  ###################
###   Ge Acquisition merge and plot   ###
#########################################

## ---------------------------- ##
from include.ReadData import *
from include.Merge import *
from include.PlotData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
## ---------------------------- ##

geDir = "../2_Decay/DataFilesGe/Decay/"
Channel = [i+1 for i in range(1024)]
Yield_Ge = Merge(geDir,"ge")

### Plot
lab = 'Ge data merged'
PlotLogy(Channel, Yield_Ge, lab)
