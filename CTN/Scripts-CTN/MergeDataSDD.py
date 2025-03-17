###############  RiP  ###################
###   SDD Acquisition merge and plot  ###
#########################################

## ---------------------------- ##
from include.ReadData import *
from include.Merge import *
from include.PlotData import *
import matplotlib.pyplot as plt
from matplotlib.pylab import *
## ---------------------------- ##

sddDir = "../2_Decay/DataFilesSDD/Decay/"
Channel = [i+1 for i in range(2048)]
Yield_Ge = Merge(sddDir,"sdd")

### Plot
lab = 'SDD data merged'
Plot(Channel, Yield_Ge, lab)