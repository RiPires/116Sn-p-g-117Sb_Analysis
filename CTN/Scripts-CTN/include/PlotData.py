############ RiP #############
##       Plot functions     ##
##############################

## ---------------------------- ##
from matplotlib.pylab import *
import matplotlib.pyplot as plt
from include.ReadData import *
## ---------------------------- ##

def Plot(x, y, lab):

    fig, ax = plt.subplots()
    ax.plot(x, y, '+-', color='k', label=lab)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    xlim(left=0.)
    ylabel('Yield', fontsize=22)
    show()

    return '-------------------'

def PlotLogy(x, y, lab):

    fig, ax = plt.subplots()
    ax.semilogy(x, y, '+-', color='k', label=lab)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

    return '-------------------'

def PlotRBS(ch, y, Label):
    
    fig, ax = plt.subplots()
    ax.semilogy(ch, y,'.-', markersize=10, color ='xkcd:magenta', label=str('Online RBS @ 155$^{\\circ}$'))
    ax.vlines(x=530, ymin=2e3, ymax=2e5, colors='red', ls='--', lw=2, label='Sn')
    ax.vlines(x=465, ymin=2e3, ymax=2e4, colors='green', ls=':', lw=2, label='Al')
    ax.vlines(x=420, ymin=2e3, ymax=2e4, colors='blue', ls='-.', lw=2, label='O')
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    #xlim(350, 550)
    ylabel('Yield', fontsize=22)
    #ylim(bottom=2e3)
    title(Label)
    show()

    return

def PlotI(t, i, lab):

    fig, ax = plt.subplots()
    ax.plot(t, i,'+-', color ='xkcd:black', label=str(lab))
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (total $\\approx$ 5 hours)',fontsize=22)
    xlim(0, 18800)
    ylabel('Current (a.u.)', fontsize=22)
    ylim(1e-10, 2e-8)
    show()

    return '-------------------'

def Plot3RateLogy(x, y1, y2, y3, lab1, lab2, lab3):

    fig, ax = plt.subplots()
    ax.semilogy(x, y1, '^-', color='k', label=lab1)
    ax.semilogy(x, y2, '*-', color='b', label=lab2)
    ax.semilogy(x, y3, '+-', color='r', label=lab3)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Rate ($s^{-1}$)', fontsize=22)
    show()
    
    return '-------------------'