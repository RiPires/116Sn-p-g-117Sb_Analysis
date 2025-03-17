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

def PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err):
    """
    Plots the reaction cross-section as a function of beam energy for different radiation types.
    
    Parameters:
    crossSections (dict): Dictionary containing cross-section values for each beam energy and radiation type.
    """

    famiano = { "Ebeam=2.2MeV": 0.00356,
                "Ebeam=2.6MeV": 0.0294,
                "Ebeam=2.9MeV": 0.0845,
                "Ebeam=3.2MeV": 0.3831,
                "Ebeam=3.6MeV": 0.7148}

    famiano_err = { "Ebeam=2.2MeV": 0.00056,
                    "Ebeam=2.6MeV": 0.0044,
                    "Ebeam=2.9MeV": 0.0145,
                    "Ebeam=3.2MeV": 0.0631,
                    "Ebeam=3.6MeV": 0.1248}
    
    ozkan = { "Ebeam=2.7MeV": 0.0409,
              "Ebeam=2.9MeV": 0.1650,
              "Ebeam=3.2MeV": 0.2380,
              "Ebeam=3.7MeV": 0.9860,
              "Ebeam=3.9MeV": 1.8200,
              "Ebeam=4.2MeV": 1.4700}
    
    ozkan_err = { "Ebeam=2.7MeV": 0.0059,
                  "Ebeam=2.9MeV": 0.0250,
                  "Ebeam=3.2MeV": 0.0580,
                  "Ebeam=3.7MeV": 0.1260,
                  "Ebeam=3.9MeV": 0.2200,
                  "Ebeam=4.2MeV": 0.2700}
    
    xarepe = {  "Ebeam=3.29MeV": 0.21,
                "Ebeam=3.66MeV": 0.7}

    xarepe_err = {  "Ebeam=3.29MeV": 0.02,
                    "Ebeam=3.66MeV": 0.1}
    
    harissopulos = {"Ebeam=2.30MeV": 0.00195,
                    "Ebeam=2.50MeV": 0.0067,
                    "Ebeam=2.70MeV": 0.0197,
                    "Ebeam=2.85MeV": 0.036,
                    "Ebeam=2.95MeV": 0.060,
                    "Ebeam=3.00MeV": 0.061,
                    "Ebeam=3.10MeV": 0.094,
                    "Ebeam=3.20MeV": 0.145,
                    "Ebeam=3.30MeV": 0.196,
                    "Ebeam=3.40MeV": 0.259,
                    "Ebeam=3.50MeV": 0.410,
                    "Ebeam=3.60MeV": 0.418,
                    "Ebeam=3.80MeV": 0.799,
                    "Ebeam=4.00MeV": 1.172,
                    "Ebeam=4.20MeV": 1.878,
                    "Ebeam=4.40MeV": 2.890,
                    "Ebeam=4.60MeV": 4.579,
                    "Ebeam=4.80MeV": 6.701,
                    "Ebeam=5.00MeV": 8.741,
                    "Ebeam=5.20MeV": 13.473}
    
    harissopulos_err = {"Ebeam=2.30MeV": 0.0003,
                        "Ebeam=2.50MeV": 0.0008,
                        "Ebeam=2.70MeV": 0.002,
                        "Ebeam=2.85MeV": 0.003,
                        "Ebeam=2.95MeV": 0.005,
                        "Ebeam=3.00MeV": 0.005,
                        "Ebeam=3.10MeV": 0.007,
                        "Ebeam=3.20MeV": 0.011,
                        "Ebeam=3.30MeV": 0.015,
                        "Ebeam=3.40MeV": 0.019,
                        "Ebeam=3.50MeV": 0.031,
                        "Ebeam=3.60MeV": 0.065,
                        "Ebeam=3.80MeV": 0.120,
                        "Ebeam=4.00MeV": 0.181,
                        "Ebeam=4.20MeV": 0.290,
                        "Ebeam=4.40MeV": 0.445,
                        "Ebeam=4.60MeV": 0.706,
                        "Ebeam=4.80MeV": 1.033,
                        "Ebeam=5.00MeV": 1.349,
                        "Ebeam=5.20MeV": 2.252}
                
    # Define colors and markers for different radiation types
    colorsHPGe = {"gamma": "xkcd:aqua", "Ka": "xkcd:light blue", "Kb": "xkcd:light green"}
    markersHPGe = {"gamma": "s", "Ka": "o", "Kb": "^"}
    colorsSDD = {"Ka": "xkcd:blue", "Kb": "xkcd:green"}
    colorsSDD_CTN = {"Ka": "xkcd:ultramarine blue", "Kb": "xkcd:electric green"}
    markersSDD = {"Ka": ".", "Kb": "v"}
    markersSDD_CTN = {"Ka": "<", "Kb": ">"}


    # Extract energy values (convert keys like "Ebeam=3.2MeV" to float values)
    energies = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in crossSections_HPGe.keys()])
    eFamiano = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in famiano.keys()])
    eOzkan = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in ozkan.keys()])
    eXarepe = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in xarepe.keys()])
    eHarissopulos = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in harissopulos.keys()])

    # Loop over each radiation type to plot separately
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ## HPGe data
    for rad_type in ["gamma", "Ka", "Kb"]:
        cross_section_values_HPGe = [crossSections_HPGe[key][rad_type] for key in crossSections_HPGe.keys()]
        hpge_err = [crossSections_HPGe_err[key][rad_type] for key in crossSections_HPGe_err.keys()]
        ax.errorbar(energies, cross_section_values_HPGe,
                    yerr=hpge_err, 
                    marker=markersHPGe[rad_type],
                    linestyle='--', 
                    linewidth=2,
                    color=colorsHPGe[rad_type], 
                    label=rad_type+" HPGe")
    ## SDD data
    for rad_type in ["Ka", "Kb"]:
        cross_section_values_SDD = [crossSections_SDD[key][rad_type] for key in crossSections_SDD.keys()]
        sdd_err = [crossSections_SDD_err[key][rad_type] for key in crossSections_SDD_err.keys()]
        ax.errorbar(energies, cross_section_values_SDD, 
                    yerr=sdd_err,
                    marker=markersSDD[rad_type],
                    linestyle='-.', 
                    color=colorsSDD[rad_type], 
                    label=rad_type+" SDD")
        
    ## SDD data CTN
    for rad_type in ["Ka", "Kb"]:
        cross_section_SDD_CTN = [crossSections_SDD_CTN[key][rad_type] for key in crossSections_SDD_CTN.keys()]
        sdd_ctn_err = [crossSections_SDD_CTN_err[key][rad_type] for key in crossSections_SDD_CTN_err.keys()]
        ax.errorbar([3.2], cross_section_SDD_CTN, 
                    yerr=sdd_ctn_err,
                    marker=markersSDD_CTN[rad_type],
                    linestyle='-.', 
                    color=colorsSDD_CTN[rad_type], 
                    label=rad_type+" SDD @ CTN")
        
    ## Famiano data
    cross_sections_Famiano = [famiano[key] for key in famiano.keys()]
    famiano_errs = [famiano_err[key] for key in famiano_err.keys()]
    ax.errorbar(eFamiano, cross_sections_Famiano, yerr=famiano_errs, marker='2', linestyle='', color="xkcd:magenta", label="Famiano 2008")

    ## Ozkan data
    cross_sections_Ozkan = [ozkan[key] for key in ozkan.keys()]
    ozkan_errs = [ozkan_err[key] for key in ozkan_err.keys()]
    ax.errorbar(eOzkan, cross_sections_Ozkan, yerr=ozkan_errs, marker='3', linestyle='', color="xkcd:lilac", label="Ozkan 2002")

    ## Xarepe data
    cross_sections_Xarepe = [xarepe[key] for key in xarepe.keys()]
    xarepe_errs = [xarepe_err[key] for key in xarepe_err.keys()]
    ax.errorbar(eXarepe, cross_sections_Xarepe, yerr=xarepe_errs, marker='*', linestyle='', color="xkcd:cranberry", label="Xarepe 2020")

    ## Harissopulos data
    cross_sections_Harissopulos = [harissopulos[key] for key in harissopulos.keys()]
    harissopulos_errs = [harissopulos_err[key] for key in harissopulos_err.keys()]
    ax.errorbar(eHarissopulos, cross_sections_Harissopulos, yerr=harissopulos_errs, marker='1', markersize=10, linestyle='', color="xkcd:pink", label="Harissopulos 2024")

    legend = ax.legend(loc="best",ncol=4,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    tick_params(axis='both', which='major', labelsize=22)
    legend.get_frame().set_facecolor('#DAEBF2')
    xlabel("Energy (MeV)", fontsize=22)
    ylabel("Cross-Section (mb)", fontsize=22)
    title("Relative Method", fontsize=22)
    show()

    return '-------------------'