## RiP

import os
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from ReadData import *

## Set accumulation adn time as zero
accu_Ka = 0.
accu_Kb = 0.
accu_t = 0.

## Set empty lists to store accumulation points and time
Accu_Ka = []
Accu_Kb = []
Accu_t = []

## Set ROI for each peak
## Ka
roiDown_Ka = int(785)
roiUp_Ka = int(835)

## Kb
roiDown_Kb = int(900)
roiUp_Kb = int(942)

## Loop over SDD data
sddPath = 'DataFilesSDD/Decay/'
for file in os.listdir(sddPath):
    y, ch = MCA2Lists(str(sddPath+file))
    ## Add Ka counts
    for c in range(roiDown_Ka, roiUp_Ka):
        accu_Ka += y[c]
    ## Add Kb counts
    for c in range(roiDown_Kb, roiUp_Kb):
        accu_Kb += y[c]
    ## Increment time
    accu_t += 15 # minutes
    ## Save integral at this point
    Accu_Ka.append(accu_Ka)
    Accu_Kb.append(accu_Kb)
    Accu_t.append(accu_t)

## Accumulation plot
fig, ax = plt.subplots()
ax.plot(Accu_t, Accu_Ka,'^-', color ='xkcd:blue', label=('Ka'))
ax.plot(Accu_t, Accu_Kb,'.-', color ='xkcd:black', label=('Kb'))
legend = ax.legend(loc="best",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Time (minutes)',fontsize=22)
ylabel('Yield', fontsize=22)
show()