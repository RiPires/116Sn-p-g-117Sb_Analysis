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
    xlabel('Channel',fontsize=22)
    ylabel('Rate ($s^{-1}$)', fontsize=22)
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

def PlotCrossSection(crossSections):
    """
    Plots the reaction cross-section as a function of beam energy for different radiation types.
    
    Parameters:
    crossSections (dict): Dictionary containing cross-section values for each beam energy and radiation type.
    """
    # Define colors and markers for different radiation types
    colors = {"gamma": "xkcd:light red", "Ka": "xkcd:light blue", "Kb": "xkcd:light green"}
    markers = {"gamma": "o", "Ka": "o", "Kb": "^"}


    # Extract energy values (convert keys like "Ebeam=3.2MeV" to float values)
    energies = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in crossSections.keys()])


    # Loop over each radiation type to plot separately
    fig, ax = plt.subplots()
    for rad_type in ["gamma", "Ka", "Kb"]:
        cross_section_values = [crossSections[key][rad_type] for key in crossSections.keys()]
        ax.semilogy(energies, cross_section_values, 
                    marker=markers[rad_type],
                    linestyle=':', 
                    color=colors[rad_type], 
                    label=rad_type)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    tick_params(axis='both', which='major', labelsize=22)
    legend.get_frame().set_facecolor('#DAEBF2')
    xlabel("Energy (MeV)", fontsize=22)
    ylabel("Cross-Section (mb)", fontsize=22)
    title("Relative Method", fontsize=22)
    show()

    return '-------------------'