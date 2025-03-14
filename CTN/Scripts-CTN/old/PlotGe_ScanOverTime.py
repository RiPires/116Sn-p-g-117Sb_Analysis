#RiP######################################
from matplotlib.pylab import *
import matplotlib.pyplot as plt
import os
from include.ReadData import*
##########################################
##########################################
def Plot():

    path = '../2_Decay/DataFilesGe/Decay/'
    f1 = '415164G2.TXT'
    f2 = '415168G2.TXT'
    f3 = '415191G2.TXT'
    f4 = '415194G2.TXT'
    f5 = '415202G2.TXT'
    f6 = '415203G2.TXT'
    f7 = '415204G2.TXT'
    f8 = '415205G2.TXT'
    f9 = '415206G2.TXT'

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

    ax1.plot(ch,y1,'^-', markersize=10, color ='xkcd:violet', label=str('1'))
    ax1.plot(ch,y2,'*-', markersize=10, color ='xkcd:magenta', label=str('2'))
    ax1.plot(ch,y3,'.-', markersize=10, color ='xkcd:pink', label=str('3'))
    ax1.plot(ch,y4,'1-', markersize=10, color ='xkcd:green', label=str('4'))
    ax1.plot(ch,y5,'2-', markersize=10, color ='xkcd:blue', label=str('5'))
    ax1.plot(ch,y6,'3-', markersize=10, color ='xkcd:red', label=str('6'))
    ax1.plot(ch,y7,'4-', markersize=10, color ='xkcd:turquoise', label=str('7'))
    ax1.plot(ch,y8,'x-', markersize=10, color ='xkcd:tangerine', label=str('8'))
    ax1.plot(ch,y9,'d-', markersize=10, color ='xkcd:vomit green', label=str('9'))

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
    ax1.set_ylim(0., 400.)
    ax2.set_xlim(150., 200.)
    ax2.set_ylim(0., 400.)

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
Plot()


