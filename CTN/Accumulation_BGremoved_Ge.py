## RiP

import os
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from ReadData import *

## Set accumulation and time as zero
accu_Ka = 0.
accu_Kb = 0.
accu_g = 0.
accu_t = 0.

## Set empty lists to store accumulation points and time
Accu_Ka = []
Accu_Kb = []
Accu_g = []
Accu_t = []

## Set ROI for each peak
## Ka
roiDown_Ka = int(36)
roiUp_Ka = int(38)
## Kb
roiDown_Kb = int(39)
roiUp_Kb = int(42)
## gamma
roiDown_g = int(160)
roiUp_g = int(164)

############################
## Calculation of bg rate ##
############################
bgFile = 'DataFilesGe/Background/415114G2.TXT'
bgYield = Ge2Lists(bgFile)[0] # counts
bgSpan = 3849. # seconds = 64 min 9 sec
bgRate = [counts/bgSpan for counts in bgYield]

## Loop over Ge data
decayTime = 900. #s = 15 min
gePath = 'DataFilesGe/Decay/'
for file in os.listdir(gePath):
    y, ch = Ge2Lists(str(gePath+file))
    ## Add Ka rate
    for c in range(roiDown_Ka, roiUp_Ka):
        accu_Ka += (y[c]/decayTime - bgRate[c])*decayTime
    ## Add Kb rate
    for c in range(roiDown_Kb, roiUp_Kb):
        accu_Kb += (y[c]/decayTime - bgRate[c])*decayTime
    ## Add gamma rate
    for c in range(roiDown_g, roiUp_g):
        accu_g += (y[c]/decayTime - bgRate[c])*decayTime
    ## Increment time
    accu_t += 15 # minutes
    ## Save rate integral at this point
    Accu_Ka.append(accu_Ka)
    Accu_Kb.append(accu_Kb)
    Accu_g.append(accu_g)
    Accu_t.append(accu_t)

## Decay rate accumulation plot
fig, ax = plt.subplots()
ax.plot(Accu_t, Accu_g,'*-', color ='xkcd:red', label=('$\gamma$ - 158 keV'))
ax.plot(Accu_t, Accu_Ka,'^-', color ='xkcd:blue', label=('K$_{\\alpha}$'))
ax.plot(Accu_t, Accu_Kb,'.-', color ='xkcd:black', label=('K$_{\\beta}$'))
legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Time (minutes)',fontsize=22)
ylabel('Yield', fontsize=22)
ylim(bottom=0.)
show()