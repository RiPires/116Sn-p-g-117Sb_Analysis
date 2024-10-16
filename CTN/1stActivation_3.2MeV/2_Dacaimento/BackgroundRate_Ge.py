#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
from ReadData import*
from MergeGe import*
##########################################

#############################
## Plot Ge backgorund rate ##
#############################

## Calculation of bg rate
bgFile = 'DataFilesGe/Background/415114G2.TXT'
bgYield = Ge2Lists(bgFile)[0] # counts
bgSpan = 3849. # seconds = 64 min 9 sec
bgRate = [counts/bgSpan for counts in bgYield]

## Calculation of background rate using the last decay data files
bgPath = 'DataFilesGe/Background_AfterDecay/'
bgAfterYield = MergeYieldGe(bgPath)
bgAfterSpan = 18000. #seconds = 20 files
bgAfterRate = [counts/bgAfterSpan for counts in bgAfterYield]

## Plot
fig, ax = plt.subplots()
ax.semilogy(Ge2Lists(bgFile)[1], bgRate,'.-', color ='xkcd:black', label= 'Background rate - Ge')
ax.semilogy(Ge2Lists(bgFile)[1], bgAfterRate,'+-', color ='xkcd:red', label= 'After Decay')
legend = ax.legend(loc="best",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Channel',fontsize=22)
ylabel('Rate ($s^{-1}$)', fontsize=22)
show()