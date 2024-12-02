#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import csv
##########################################
##########################################

File = '../1_Irradiation/DataFiles/Sn116-pg-240516_CurrentMonitor.dat'
with open(File, 'r') as file:
    reader = csv.reader(file, delimiter='\n', skipinitialspace=True)
    data = list(reader)
time = []
current = []
aux = []

for i in range(len(data)):
    aux.append(data[i][0].split())
for i in range(len(aux)):
    time.append(float(aux[i][0]))
    current.append(float(aux[i][1]))

fig, ax = plt.subplots()
#ax.plot(time, current,'.-', color ='xkcd:black')
ax.semilogy(time, current,'-', color ='xkcd:red', label='H$^{+}$ beam current')
legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
legend.get_frame().set_facecolor('#DAEBF2')
tick_params(axis='both', which='major', labelsize=22)
xlabel('Time (total $\\approx$ 5 hours)',fontsize=22)
xlim(0, 18800)
ylabel('Current (a.u.)', fontsize=22)
ylim(1e-10, 2e-8)
show()

