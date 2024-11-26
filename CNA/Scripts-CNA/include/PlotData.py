############ RiP #############
##       Plot functions     ##
##############################

## ---------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
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
    xlim(left=0.)
    ylabel('Yield', fontsize=22)
    show()

    return '-------------------'

def PlotRateLogy(x, y, lab):

    fig, ax = plt.subplots()
    ax.semilogy(x, y, '+-', color='k', label=lab)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy (keV)',fontsize=22)
    xlim(left=0.)
    ylabel('Rate ($s^{-1}$)', fontsize=22)
    show()

    return '-------------------'

def PlotBothRateLogy(x, y1, y2, lab1, lab2):

    fig, ax = plt.subplots()
    ax.semilogy(x, y1, '+-', color='k', label=lab1)
    ax.semilogy(x, y2, '*-', color='b', label=lab2)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy (keV)',fontsize=22)
    xlim(left=0.)
    ylabel('Rate ($s^{-1}$)', fontsize=22)
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
    xlabel('Energy (keV)',fontsize=22)
    xlim(left=0.)
    ylabel('Rate ($s^{-1}$)', fontsize=22)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    figure=gcf()
    figure.set_size_inches(16,9)
    savefig(fname=str(lab3+'.svg'), dpi=200, format='svg')
    show()
    

    return '-------------------'

def PlotI(t, i, lab):

    fig, ax = plt.subplots()
    ax.plot(t, i,'+-', color ='xkcd:black', label=str(lab))
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Time (sec since 00h00)',fontsize=22)
    ylabel('Current (nA)', fontsize=22)
    ylim(0,200)
    show()

    return '-------------------'

def PlotRBS(ch, y, lab):

    fig, ax = plt.subplots()
    ax.semilogy(ch, y,'+-', color ='xkcd:black', label=str(lab))
    legend = ax.legend(loc="best",ncol=2,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel',fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

    return '-------------------'