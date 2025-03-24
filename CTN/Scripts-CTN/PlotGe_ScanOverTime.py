#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
import random
import itertools
##########################################
##########################################

##########################################
##########################################
def PlotAll():

    ch = [(i+1) for i in range(1024)]
    path = '../2_Decay/DataFilesGe/BgRemoved/'
    
    nr_colors = len(os.listdir(path))
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(nr_colors)]
    markers = itertools.cycle((".", ",", "o", "v", "^", "<", ">", "1", "2", 
               "3", "4", "8", "s", "p", "*", "h", "+","x", "d"))
    counter = 0

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False)
    for file in sorted(os.listdir(path)):
        y = Ge2Lists(path+file)[0]
        ax1.plot(ch, y, linestyle=":", marker=next(markers), color =colors[counter], label=file.replace(".TXT",""))
        ax2.plot(ch, y, linestyle=":", marker=next(markers), color =colors[counter])
        counter+=1
    ax1.set_xlim(20., 50.)
    ax1.set_ylim(0., 3500.)
    ax2.set_xlim(150., 200.)
    ax2.set_ylim(0., 3500.)

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

    #legend1 = ax1.legend(loc="upper left",ncol=1, shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Channel", fontsize=22, labelpad=20)
    plt.ylabel("Yield", fontsize=22, labelpad=45)

    show()

    return

## Plot
PlotAll()


def Plot():

    path = '../2_Decay/DataFilesGe/BgRemoved/'
    f1 = '415164G2_BgRemoved.TXT'
    f2 = '415168G2_BgRemoved.TXT'
    f3 = '415131G2_BgRemoved.TXT'
    f4 = '415150G2_BgRemoved.TXT'
    f5 = '415151G2_BgRemoved.TXT'
    f6 = '415129G2_BgRemoved.TXT'
    f7 = '415128G2_BgRemoved.TXT'
    f8 = '415132G2_BgRemoved.TXT'
    f9 = '415127G2_BgRemoved.TXT'

    y1, ch = Ge2Lists(str(path+f1))
    y2 = Ge2Lists(str(path+f2))[0]
    y3= Ge2Lists(str(path+f3))[0]
    y4= Ge2Lists(str(path+f4))[0]
    y5= Ge2Lists(str(path+f5))[0]
    y6= Ge2Lists(str(path+f6))[0]
    y7= Ge2Lists(str(path+f7))[0]
    y8= Ge2Lists(str(path+f8))[0]
    y9= Ge2Lists(str(path+f9))[0] 

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=False)

    ax1.plot(ch,y1,'^-', markersize=10, color ='xkcd:violet', label=f1)
    ax1.plot(ch,y2,'*-', markersize=10, color ='xkcd:magenta', label=f2)
    ax1.plot(ch,y3,'.-', markersize=10, color ='xkcd:pink', label=f3)
    ax1.plot(ch,y4,'1-', markersize=10, color ='xkcd:green', label=f4)
    ax1.plot(ch,y5,'2-', markersize=10, color ='xkcd:blue', label=f5)
    ax1.plot(ch,y6,'3-', markersize=10, color ='xkcd:red', label=f6)
    ax1.plot(ch,y7,'4-', markersize=10, color ='xkcd:turquoise', label=f7)
    ax1.plot(ch,y8,'x-', markersize=10, color ='xkcd:tangerine', label=f8)
    ax1.plot(ch,y9,'d-', markersize=10, color ='xkcd:vomit green', label=f9)

    ax2.plot(ch,y1,'^-', markersize=10, color ='xkcd:violet')
    ax2.plot(ch,y2,'*-', markersize=10, color ='xkcd:magenta')
    ax2.plot(ch,y3,'.-', markersize=10, color ='xkcd:pink')
    ax2.plot(ch,y4,'1-', markersize=10, color ='xkcd:green', label=str('9 hours'))
    ax2.plot(ch,y5,'2-', markersize=10, color ='xkcd:blue', label=str('9 hours'))
    ax2.plot(ch,y6,'3-', markersize=10, color ='xkcd:red', label=str('9 hours'))
    ax2.plot(ch,y7,'4-', markersize=10, color ='xkcd:turquoise', label=str('9 hours'))
    ax2.plot(ch,y8,'x-', markersize=10, color ='xkcd:tangerine', label=str('9 hours'))
    ax2.plot(ch,y9,'d-', markersize=10, color ='xkcd:vomit green', label=str('9 hours'))

    ax1.set_xlim(20., 50.)
    ax1.set_ylim(0., 2000.)
    ax2.set_xlim(150., 200.)
    ax2.set_ylim(0., 2000.)

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

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Channel", fontsize=22, labelpad=20)
    plt.ylabel("Yield", fontsize=22, labelpad=45)

    show()

    return

## Plot
#Plot()


