#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
##########################################
##########################################
def Plot():

    path = '../2_Decay/DataFilesGe/Decay/'
    min5 = '415119G2.TXT'
    hor3 = '415130G2.TXT'
    hor10 = '415150G2.TXT'
    hor10 = '415150G2.TXT'

    y1, ch = Ge2Lists(str(path+min5))
    y2 = Ge2Lists(str(path+hor3))[0]
    y3= Ge2Lists(str(path+hor10))[0] 

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False)

    ax1.plot(ch,y1,'^-', markersize=10, color ='xkcd:violet', label=str('30 min'))
    ax1.plot(ch,y2,'*-', markersize=10, color ='xkcd:magenta', label=str('1 hour'))
    ax1.plot(ch,y3,'.-', markersize=10, color ='xkcd:pink', label=str('9 hours'))
    ax1.vlines(x=36., ymin=0., ymax=4000., colors='xkcd:gold', ls='--', lw=2)
    ax1.vlines(x=39.5, ymin=0., ymax=4000., colors='xkcd:poo', ls=':', lw=2)

    ax2.plot(ch,y1,'^-', markersize=10, color ='xkcd:violet')
    ax2.plot(ch,y2,'*-', markersize=10, color ='xkcd:magenta')
    ax2.plot(ch,y3,'.-', markersize=10, color ='xkcd:pink')
    ax2.vlines(x=36., ymin=0., ymax=4000., colors='xkcd:gold', ls='--', lw=2, label='E$_{K_{\\alpha}} \\approx$ 25.2 keV')
    ax2.vlines(x=39.5, ymin=0., ymax=4000., colors='xkcd:poo', ls=':', lw=2, label='E$_{K_{\\beta}} \\approx$ 28.4 keV')
    ax2.vlines(x=162.5, ymin=0., ymax=4000., colors='xkcd:rusty orange', ls='-.', lw=2, label='E$_\gamma\\ \\approx$ 158 keV')
    ax2.vlines(x=186., ymin=0., ymax=2000., colors='xkcd:orange', ls='solid', lw=2, label='K$_{\\alpha} + \gamma$')

    ax1.set_xlim(20., 50.)
    ax1.set_ylim(0., 4200.)
    ax2.set_xlim(150., 200.)
    ax2.set_ylim(0., 4200.)

    # hide the spines between ax and ax2
    ax1.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax1.yaxis.tick_left()
    ax1.tick_params(labelleft='off')
    ax2.yaxis.tick_right()
    ax2.axes.get_yaxis().set_visible(False)

    ax1.tick_params(axis='both', which='major', labelsize=22)
    ax2.tick_params(axis='both', which='major', labelsize=22)

    d = .01  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((1-d, 1+d), (-d, +d), **kwargs)
    ax1.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1-d, 1+d), **kwargs)
    ax2.plot((-d, +d), (-d, +d), **kwargs)

    legend1 = ax1.legend(loc="upper left",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend2 = ax2.legend(loc="upper right",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Channel", fontsize=22, labelpad=20)
    plt.ylabel("Yield", fontsize=22, labelpad=45)

    show()

    return

## Plot
Plot()


