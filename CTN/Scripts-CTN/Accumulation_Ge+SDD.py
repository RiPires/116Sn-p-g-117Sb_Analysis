## RiP

import os
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from ReadData import *

##################################
## Calculations for Ge detector ##
##################################

## Set accumulation and time as zero ##
ge_accu_Ka = 0.
ge_accu_Kb = 0.
ge_accu_g = 0.
ge_accu_t = 0.

## Set empty lists to store accumulation points and time ##
ge_Accu_Ka = []
ge_Accu_Kb = []
ge_Accu_g = []
ge_Accu_t = []

## Set ROI for each peak ##
## Ka
ge_roiDown_Ka = int(36)
ge_roiUp_Ka = int(38)
## Kb
ge_roiDown_Kb = int(39)
ge_roiUp_Kb = int(42)
## gamma
ge_roiDown_g = int(160)
ge_roiUp_g = int(164)

## Calculation of ge bg rate ##
bgFile = '../Calibration/BEGe-Calib/Background/415114G2.TXT'
bgYield = Ge2Lists(bgFile)[0] # counts
bgSpan = 3849. # seconds = 64 min 9 sec
bgRate = [counts/bgSpan for counts in bgYield]

## Loop over Ge data
decayTime = 900. #s = 15 min
gePath = '../2_Decay/DataFilesGe/Decay/'
for file in os.listdir(gePath):
    y, ch = Ge2Lists(str(gePath+file))
    ## Add Ka rate
    for c in range(ge_roiDown_Ka, ge_roiUp_Ka):
        ge_accu_Ka += (y[c]/decayTime - bgRate[c])
    ## Add Kb rate
    for c in range(ge_roiDown_Kb, ge_roiUp_Kb):
        ge_accu_Kb += (y[c]/decayTime - bgRate[c])
    ## Add gamma rate
    for c in range(ge_roiDown_g, ge_roiUp_g):
        ge_accu_g += (y[c]/decayTime - bgRate[c])
    ## Increment time
    ge_accu_t += 15 # minutes
    ## Save rate integral at this point
    ge_Accu_Ka.append(ge_accu_Ka)
    ge_Accu_Kb.append(ge_accu_Kb)
    ge_Accu_g.append(ge_accu_g)
    ge_Accu_t.append(ge_accu_t)
##################################################################
##################################################################

###################################
## Calculations for SDD detector ##
###################################

## Set accumulation adn time as zero
sdd_accu_Ka = 0.
sdd_accu_Kb = 0.
sdd_accu_t = 0.

## Set empty lists to store accumulation points and time
sdd_Accu_Ka = []
sdd_Accu_Kb = []
sdd_Accu_t = []

## Set ROI for each peak
## Ka
sdd_roiDown_Ka = int(785)
sdd_roiUp_Ka = int(835)

## Kb
sdd_roiDown_Kb = int(900)
sdd_roiUp_Kb = int(942)

## Loop over SDD data
sddPath = '../2_Decay/DataFilesSDD/Decay/'
for file in os.listdir(sddPath):
    y, ch = MCA2Lists(str(sddPath+file))
    ## Add Ka counts
    for c in range(sdd_roiDown_Ka, sdd_roiUp_Ka):
        sdd_accu_Ka += y[c]/decayTime
    ## Add Kb counts
    for c in range(sdd_roiDown_Kb, sdd_roiUp_Kb):
        sdd_accu_Kb += y[c]/decayTime
    ## Increment time
    sdd_accu_t += 15 # minutes
    ## Save integral at this point
    sdd_Accu_Ka.append(sdd_accu_Ka)
    sdd_Accu_Kb.append(sdd_accu_Kb)
    sdd_Accu_t.append(sdd_accu_t)

###########################################################################
## Decay rate normalized accumulation plot for both Ge and SDD detectors ##
########################################################################### 

fig, ax = plt.subplots()
## Ge
ax.semilogy(ge_Accu_t, ge_Accu_Ka,'d-', markersize=8, color ='xkcd:gold', label=('Ge det.: K$_{\\alpha}$'))
ax.semilogy(ge_Accu_t, ge_Accu_Kb,'*-', color ='xkcd:poo', label=('Ge det.: K$_{\\beta}$'))
ax.semilogy(ge_Accu_t, ge_Accu_g,'.-', markersize=8, color ='xkcd:rusty orange', label=('Ge det.: $\gamma$'))
# SDD
ax.semilogy(sdd_Accu_t, sdd_Accu_Ka,'^-', color ='xkcd:violet', label=('SDD det.: K$_{\\alpha}$'))
ax.semilogy(sdd_Accu_t, sdd_Accu_Kb,'v-', color ='xkcd:magenta', label=('SDD det.: K$_{\\beta}$'))
legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Time (minutes)',fontsize=22)
xlim(0., 1000.)
ylabel('Accumulation Yield', fontsize=22)
show()