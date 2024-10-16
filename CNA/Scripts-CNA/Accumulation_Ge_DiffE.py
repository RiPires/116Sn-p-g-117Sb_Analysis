#############################  RiP  #################################
###   Function to perform the accumulation of decay measurement   ###
###   for each activation energy and plot                         ###
#####################################################################

## ------------------------------ ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from Accumulation import *
## ------------------------------ ##

##  Define path for each activation energy
e32path = 'Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/'
e35path = 'Ebeam=3.5MeV/2_Decay/DataFiles_HPGe/'
e39path = 'Ebeam=3.9MeV/2_Decay/DataFiles_HPGe/'
e43path = 'Ebeam=4.3MeV/2_Decay/DataFiles_HPGe/'
e47path = 'Ebeam=4.7MeV/2_Decay/DataFiles_HPGe/'
e50path = 'Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/'

##  Perform accumulation for each energy
Accu_Ka32, Accu_Kb32, Accu_g32, Accu_t32 = AccumulateGe(e32path)
Accu_Ka35, Accu_Kb35, Accu_g35, Accu_t35 = AccumulateGe(e35path)
Accu_Ka39, Accu_Kb39, Accu_g39, Accu_t39 = AccumulateGe(e39path)
Accu_Ka43, Accu_Kb43, Accu_g43, Accu_t43 = AccumulateGe(e43path)
Accu_Ka47, Accu_Kb47, Accu_g47, Accu_t47 = AccumulateGe(e47path)
Accu_Ka50, Accu_Kb50, Accu_g50, Accu_t50 = AccumulateGe(e50path)

## Accumulation plot
fig, ax = plt.subplots()
## 5.= MeV
ax.semilogy(Accu_t50, Accu_g50,'*-', color ='xkcd:pale red', label=('E$_{beam}$ = 5.0 MeV'))
ax.semilogy(Accu_t50, Accu_Ka50,'^-', color ='xkcd:pinkish red')
#ax.semilogy(Accu_t50, Accu_Kb50,'.-', color ='xkcd:black', label=('Kb'))
## 4.7 MeV
ax.semilogy(Accu_t47, Accu_g47,'*-', color ='xkcd:dull yellow', label=('E$_{beam}$ = 4.7 MeV'))
ax.semilogy(Accu_t47, Accu_Ka47,'^-', color ='xkcd:amber')
#ax.semilogy(Accu_t47, Accu_Kb47,'.-', color ='xkcd:black', label=('Kb'))
## 4.3 MeV
ax.semilogy(Accu_t43, Accu_g43,'*-', color ='xkcd:gold', label=('E$_{beam}$ = 4.3 MeV'))
ax.semilogy(Accu_t43, Accu_Ka43,'^-', color ='xkcd:light orange')
#ax.semilogy(Accu_t43, Accu_Kb43,'.-', color ='xkcd:black', label=('Kb'))
## 3.9 MeV
ax.semilogy(Accu_t39, Accu_g39,'*-', color ='xkcd:sea green', label=('E$_{beam}$ = 3.9 MeV'))
ax.semilogy(Accu_t39, Accu_Ka39,'^-', color ='xkcd:lime')
#ax.semilogy(Accu_t39, Accu_Kb39,'.-', color ='xkcd:black', label=('Kb'))
## 3.5 MeV
ax.semilogy(Accu_t35, Accu_g35,'*-', color ='xkcd:magenta', label=('E$_{beam}$ = 3.5 MeV'))
ax.semilogy(Accu_t35, Accu_Ka35,'^-', color ='xkcd:pink')
#ax.semilogy(Accu_t35, Accu_Kb35,'.-', color ='xkcd:black', label=('Kb'))
## 3.2 MeV
ax.semilogy(Accu_t32, Accu_g32,'*-', color ='xkcd:navy blue', label=('E$_{beam}$ = 3.2 MeV'))
ax.semilogy(Accu_t32, Accu_Ka32,'^-', color ='xkcd:light blue')
#ax.semilogy(Accu_t32, Accu_Kb32,'.-', color ='xkcd:black', label=('Kb'))
legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Time (minutes)',fontsize=22)
xlim(0, 1000)
ylabel('Yield', fontsize=22)
ylim(1e3, 5e7)
show()