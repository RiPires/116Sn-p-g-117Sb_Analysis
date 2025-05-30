############ RiP #############
##       Plot functions     ##
##############################

## ---------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
## ---------------------------- ##

# ::::::::::::::::::::::::::::::::::::::::::::::: #
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
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
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
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
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
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
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
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
def Plot3RateLogy(x, y1, y2, y3, lab1, lab2, lab3):

    energies = [(x[i]*0.3225-0.149) for i in range(len(x))]
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(energies, y1, '^-', color='k', label=lab1)
    ax.plot(energies, y2, '*-', color='b', label=lab2)
    ax.plot(energies, y3, '+-', color='r', label=lab3)
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy [keV]',fontsize=22)
    ylabel('Count Rate ($\\rm{s}^{\\rm{-1}}$)', fontsize=22)
    show()
    

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
def PlotI(t, i, lab):

    fig, ax = plt.subplots()
    ax.plot(t, i,'+', color ='xkcd:black', label=str(lab))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Irradiation time [s]',fontsize=22)
    ylabel('Beam Current [nA]', fontsize=22)
    #ylim(0,200)
    show()

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
def Plot6I(t, i, lab):

    colors = ['xkcd:black', 'xkcd:red', 'xkcd:blue', 'xkcd:green', 'xkcd:pink', 'xkcd:yellow']
    markers = ['1', '2', '3', '+', 'v', '^']
    fig, ax = plt.subplots()
    for k in range(len(i)-1, -1, -1):
        ax.plot(t[k], i[k], markers[k], color=colors[k], label=str(lab[k]))
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Irradiation Time [s]',fontsize=22)
    ylabel('Beam Current [nA]', fontsize=22)
    ylim(0,250)
    show()

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
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
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
def Plot6RBS(ch, y, lab):

    colors = ['xkcd:black', 'xkcd:red', 'xkcd:blue', 'xkcd:green', 'xkcd:pink', 'xkcd:yellow']
    markers = ['1-', '2-', '3-', '+-', 'v-', '^-']
    fig, ax = plt.subplots()
    # Prepare the list of yields in the same order as labs
    y_list = [y[key] for key in lab]
    for k in range(len(y_list)-1, -1, -1):
        ax.semilogy(ch, y_list[k], markers[k], color=colors[k], label=str(lab[k]))
    legend = ax.legend(loc="best", ncol=1, shadow=False, fancybox=True, framealpha=0.0, fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Channel', fontsize=22)
    ylabel('Yield', fontsize=22)
    show()

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #

# ::::::::::::::::::::::::::::::::::::::::::::::: #
def PlotMyCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE):
    """
    Plots the reaction cross-section as a function of beam energy for different radiation types.
    
    Parameters:
    crossSections (dict): Dictionary containing cross-section values for each beam energy and radiation type.
    """
                
    # Define colors and markers for different radiation types
    colorsHPGe = {"gamma": "xkcd:light green", "Ka": "xkcd:blue", "Kb": "xkcd:light red", "511 keV": "xkcd:purple", "861 keV": "xkcd:mustard", "1004 keV": "xkcd:light orange"}
    markersHPGe = {"gamma": "s", "Ka": "o", "Kb": "^", "511 keV": "+", "861 keV": "P", "1004 keV": "X"}
    colorsBEGe_CTN = {"gamma": "xkcd:cyan", "Ka": "xkcd:sky blue", "Kb": "xkcd:pale green"}
    markersBEGe_CTN = {"gamma": "d", "Ka": "p", "Kb": "P"}
    colorsSDD = {"Ka": "xkcd:sky", "Kb": "xkcd:pink"}
    colorsSDD_CTN = {"Ka": "xkcd:ultramarine blue", "Kb": "xkcd:electric green"}
    markersSDD = {"Ka": "*", "Kb": "v"}
    markersSDD_CTN = {"Ka": "<", "Kb": ">"}

    # Extract energy values (convert keys like "Ebeam=3.2MeV" to float values)
    energies = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in crossSections_HPGe.keys()])

    # Loop over each radiation type to plot separately
    labs = {"gamma": "$\\gamma_{158}$", "Ka": "$K_{\\alpha}$", "Kb": "$K_{\\beta}$", "511 keV": "$\\gamma_{511}$", "861 keV": "$\\gamma_{861}$", "1004 keV": "$\\gamma_{1004}$"}
    fig, ax = plt.subplots()
    ax.set_yscale("log")

    ## HPGe at CNA data
    for rad_type in ["Ka", "Kb", "gamma", "511 keV", "861 keV", "1004 keV"]:
        cross_section_values_HPGe = [crossSections_HPGe[key][rad_type] for key in crossSections_HPGe.keys()]
        hpge_err = [crossSections_HPGe_err[key][rad_type] for key in crossSections_HPGe_err.keys()]
        ax.errorbar(energies, cross_section_values_HPGe,
                    #xerr=dE,
                    yerr=hpge_err,
                    capsize=4,
                    marker=markersHPGe[rad_type],
                    linestyle='--', 
                    linewidth=2,
                    color=colorsHPGe[rad_type], 
                    label=labs[rad_type]+" HPGe@CNA")
        
    ## SDD at CNA data
    for rad_type in ["Ka", "Kb"]:
        cross_section_values_SDD = [crossSections_SDD[key][rad_type] for key in crossSections_SDD.keys()]
        sdd_err = [crossSections_SDD_err[key][rad_type] for key in crossSections_SDD_err.keys()]
        ax.errorbar(energies, cross_section_values_SDD, 
                    #xerr=dE,
                    yerr=sdd_err,
                    capsize=4,
                    marker=markersSDD[rad_type],
                    linestyle='-.', 
                    linewidth=2,
                    color=colorsSDD[rad_type], 
                    label=labs[rad_type]+" SDD@CNA")
    
    ## BEGe at CTN data
    """     for rad_type in ["gamma", "Ka", "Kb"]:
        cross_section_BEGe = [crossSections_BEGe[key][rad_type] for key in crossSections_BEGe.keys()]
        bege_ctn_err = [crossSections_BEGe_err[key][rad_type] for key in crossSections_BEGe_err.keys()]
        ax.errorbar([3.215], cross_section_BEGe, 
                    yerr=bege_ctn_err,
                    capsize=4,
                    marker=markersBEGe_CTN[rad_type],
                    linestyle='', 
                    linewidth=2,
                    color=colorsBEGe_CTN[rad_type], 
                    label=labs[rad_type]+" BEGe@CTN") """
        
    ## SDD at CTN data
    """     for rad_type in ["Ka", "Kb"]:
        cross_section_SDD_CTN = [crossSections_SDD_CTN[key][rad_type] for key in crossSections_SDD_CTN.keys()]
        sdd_ctn_err = [crossSections_SDD_CTN_err[key][rad_type] for key in crossSections_SDD_CTN_err.keys()]
        ax.errorbar([3.215], cross_section_SDD_CTN, 
                    yerr=sdd_ctn_err,
                    capsize=4,
                    marker=markersSDD_CTN[rad_type],
                    linestyle='', 
                    linewidth=2,
                    color=colorsSDD_CTN[rad_type], 
                    label=labs[rad_type]+" SDD@CTN") """

    ## Organize data labels
    handles,labels = ax.get_legend_handles_labels()

    #for i in range(len(labels)):
    #   print(f"{labels[i]} \t\t {i}")

    #handles = [handles[4],  handles[5],  handles[14], 
    #           handles[2],  handles[3],  handles[1],  
    #           handles[7],  handles[8],  handles[6], 
    #           handles[9],  handles[10], handles[13], 
    #           handles[11], handles[12], handles[0]]
    
    #labels = [labels[4],  labels[5],  labels[14], 
    #           labels[2],  labels[3],  labels[1],  
    #           labels[7],  labels[8],  labels[6], 
    #           labels[9],  labels[10], labels[13], 
    #           labels[11], labels[12], labels[0]]
    
    legend = ax.legend(handles, labels, loc="upper left",ncol=3,shadow=False,fancybox=True,framealpha = 0.0,fontsize=14)
    tick_params(axis='both', which='major', labelsize=22)
    legend.get_frame().set_facecolor('#DAEBF2')
    xlabel("$E_{\\rm{beam}}$ [MeV]", fontsize=22)
    ylabel("Cross-Section [mb]", fontsize=22)
    #ylim(0, 1e3)
    title("Relative Method", fontsize=22)
    show() 

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #

def PlotCrossSection(crossSections_HPGe, crossSections_HPGe_err, crossSections_SDD, crossSections_SDD_err, crossSections_BEGe, crossSections_BEGe_err, crossSections_SDD_CTN, crossSections_SDD_CTN_err, dE):
    """
    Plots the reaction cross-section as a function of beam energy for different radiation types.
    
    Parameters:
    crossSections (dict): Dictionary containing cross-section values for each beam energy and radiation type.
    """

    # Collect all energies from all dictionaries
    all_energy_keys = set()
    for d in [crossSections_HPGe, crossSections_SDD]:
        all_energy_keys.update(d.keys())
    # Sort energies numerically
    def energy_float(key):
        return float(key.replace("Ebeam=", "").replace("MeV", ""))
    sorted_keys = sorted(all_energy_keys, key=energy_float)
    energies = [energy_float(k) for k in sorted_keys]

    means, stds = [], []
    for key in sorted_keys:
        vals = []
        errs = []
        # HPGe
        if key in crossSections_HPGe:
            for rad_type in ["gamma", "Ka", "Kb"]:
                if rad_type in crossSections_HPGe[key]:
                    vals.append(crossSections_HPGe[key][rad_type])
                    errs.append(crossSections_HPGe_err[key][rad_type])
        # SDD
        if key in crossSections_SDD:
            for rad_type in ["Ka", "Kb"]:
                if rad_type in crossSections_SDD[key]:
                    vals.append(crossSections_SDD[key][rad_type])
                    errs.append(crossSections_SDD_err[key][rad_type])
        # Weighted average
        if vals and errs and all(e > 0 for e in errs):
            weights = [1/(e**2) for e in errs]
            mean = np.average(vals, weights=weights)
            std = np.sqrt(1/np.sum(weights))
            means.append(mean)
            stds.append(std)
        elif vals:
            means.append(np.mean(vals))
            stds.append(np.std(vals))
        else:
            means.append(np.nan)
            stds.append(np.nan)

    ##                              [ value ,  error ] 
    famiano = {     "Ebeam=2.2MeV": [0.00356, 0.00056],
                    "Ebeam=2.6MeV": [0.0294,  0.0044],
                    "Ebeam=2.9MeV": [0.0845,  0.0145],
                    "Ebeam=3.2MeV": [0.3831,  0.0631],
                    "Ebeam=3.6MeV": [0.7148,  0.1248]}

    ozkan = {       "Ebeam=2.7MeV": [0.0409, 0.0059],
                    "Ebeam=2.9MeV": [0.1650, 0.0250],
                    "Ebeam=3.2MeV": [0.2380, 0.0580],
                    "Ebeam=3.4MeV": [0.4974, 0.0965],
                    "Ebeam=3.7MeV": [0.9860, 0.1260],
                    "Ebeam=3.9MeV": [1.8200, 0.2200],
                    "Ebeam=4.2MeV": [1.4700, 0.2700]}

    xarepe = {      "Ebeam=2.80MeV": [0.0228, 0.0033],
                    "Ebeam=3.29MeV": [0.1466, 0.0125],
                    "Ebeam=3.66MeV": [0.5088, 0.0349]}
    
    harissopulos = {"Ebeam=2.30MeV": [0.00195, 0.0003],
                    "Ebeam=2.3MeV" : [0.0018, 0.0003],
                    "Ebeam=2.45MeV": [0.0046, 0.0007],
                    "Ebeam=2.50MeV": [0.0067, 0.0008],
                    "Ebeam=2.70MeV": [0.0197, 0.002],
                    "Ebeam=2.85MeV": [0.036, 0.003],
                    "Ebeam=2.95MeV": [0.060, 0.005],
                    "Ebeam=3.00MeV": [0.061, 0.005],
                    "Ebeam=3.10MeV": [0.094, 0.007],
                    "Ebeam=3.20MeV": [0.145, 0.011],
                    "Ebeam=3.30MeV": [0.196, 0.015],
                    "Ebeam=3.40MeV": [0.259, 0.019],
                    "Ebeam=3.5MeV" : [0.305, 0.052],
                    "Ebeam=3.50MeV": [0.410, 0.031],
                    "Ebeam=3.60MeV": [0.418, 0.065],
                    "Ebeam=3.80MeV": [0.799, 0.120],
                    "Ebeam=4.00MeV": [1.172, 0.181],
                    "Ebeam=4.20MeV": [1.878, 0.290],
                    "Ebeam=4.40MeV": [2.890, 0.445],
                    "Ebeam=4.60MeV": [4.579, 0.706],
                    "Ebeam=4.80MeV": [6.701, 1.033],
                    "Ebeam=5.00MeV": [8.741, 1.349],
                    "Ebeam=5.20MeV": [13.473, 2.252]}
    
    talys = [8.373980E-04,
            1.649710E-03,
            3.108450E-03,
            5.627350E-03,
            9.826080E-03,
            1.660520E-02,
            2.723810E-02,
            4.348120E-02,
            6.770310E-02,
            1.030320E-01,
            1.535200E-01,
            2.243280E-01,
            3.219130E-01,
            4.542390E-01,
            6.309800E-01,
            8.637270E-01,
            1.166250E+00,
            1.554440E+00,
            2.046780E+00,
            2.664280E+00,
            3.430530E+00,
            4.371740E+00,
            5.516640E+00,
            6.896220E+00,
            8.543560E+00,
            1.049330E+01,
            1.278110E+01,
            1.544310E+01,
            1.851470E+01,
            2.203030E+01,
            2.602170E+01,
            3.051710E+01,
            3.554040E+01,
            4.110990E+01]
    
    talysEnergies = [2.200000E+00,
                    2.300000E+00,
                    2.400000E+00,
                    2.500000E+00,
                    2.600000E+00,
                    2.700000E+00,
                    2.800000E+00,
                    2.900000E+00,
                    3.000000E+00,
                    3.100000E+00,
                    3.200000E+00,
                    3.300000E+00,
                    3.400000E+00,
                    3.500000E+00,
                    3.600000E+00,
                    3.700000E+00,
                    3.800000E+00,
                    3.900000E+00,
                    4.000000E+00,
                    4.100000E+00,
                    4.200000E+00,
                    4.300000E+00,
                    4.400000E+00,
                    4.500000E+00,
                    4.600000E+00,
                    4.700000E+00,
                    4.800000E+00,
                    4.900000E+00,
                    5.000000E+00,
                    5.100000E+00,
                    5.200000E+00,
                    5.300000E+00,
                    5.400000E+00,
                    5.500000E+00]

    # Extract energy values (convert keys like "Ebeam=3.2MeV" to float values)
    eFamiano = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in famiano.keys()])
    eOzkan = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in ozkan.keys()])
    eXarepe = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in xarepe.keys()])
    eHarissopulos = sorted([float(key.replace("Ebeam=", "").replace("MeV", "")) for key in harissopulos.keys()])

    print(f"Averaged cross-sections for {len(means)} energies:")
    for i, energy in enumerate(energies):
        if not np.isnan(means[i]):
            print(f"Ebeam={energy:.1f} MeV: {means[i]:.4f} mb ± {stds[i]:.4f} mb")
        else:
            print(f"Ebeam={energy:.1f} MeV: No data available")
    # Loop over each radiation type to plot separately
    fig, ax = plt.subplots()
    ax.set_yscale("log")

    ## Experimental mean cross-section
    ax.errorbar(energies, means, yerr=stds, 
                capsize=4, marker='o', 
                linestyle='', color="xkcd:green", 
                label="Experimental averaged")

    ## Famiano data
    cross_sections_Famiano = [famiano[key][0] for key in famiano.keys()]
    famiano_errs = [famiano[key][1] for key in famiano.keys()]
    ax.errorbar(eFamiano, cross_sections_Famiano, yerr=famiano_errs, capsize=4, marker='2', markersize=10, linestyle='', color="xkcd:magenta", label="Famiano 2008")

    ## Ozkan data
    cross_sections_Ozkan = [ozkan[key][0] for key in ozkan.keys()]
    ozkan_errs = [ozkan[key][1] for key in ozkan.keys()]
    ax.errorbar(eOzkan, cross_sections_Ozkan, yerr=ozkan_errs, capsize=4, marker='3', markersize=10, linestyle='', color="xkcd:lilac", label='$\\rm{\\"{O}}$zkan 2002')

    ## Xarepe data
    cross_sections_Xarepe = [xarepe[key][0] for key in xarepe.keys()]
    xarepe_errs = [xarepe[key][1] for key in xarepe.keys()]
    ax.errorbar(eXarepe, cross_sections_Xarepe, yerr=xarepe_errs, capsize=4, marker='*', linestyle='', color="xkcd:browny orange", label="Xarepe 2021")

    ## Harissopulos data
    cross_sections_Harissopulos = [harissopulos[key][0] for key in harissopulos.keys()]
    harissopulos_errs = [harissopulos[key][1] for key in harissopulos.keys()]
    ax.errorbar(eHarissopulos, cross_sections_Harissopulos, yerr=harissopulos_errs, capsize=4, marker='1', markersize=10, linestyle='', color="xkcd:pink", label="Harissopulos 2024")

    ## Talys data
    ax.plot(talysEnergies, talys, linestyle='-', color="xkcd:black", label="Talys 2.0")

    ## Organize data labels
    handles,labels = ax.get_legend_handles_labels()

    #for i in range(len(labels)):
    #   print(f"{labels[i]} \t\t {i}")

    #handles = [handles[4],  handles[5],  handles[14], 
    #           handles[2],  handles[3],  handles[1],  
    #           handles[7],  handles[8],  handles[6], 
    #           handles[9],  handles[10], handles[13], 
    #           handles[11], handles[12], handles[0]]
    
    #labels = [labels[4],  labels[5],  labels[14], 
    #           labels[2],  labels[3],  labels[1],  
    #           labels[7],  labels[8],  labels[6], 
    #           labels[9],  labels[10], labels[13], 
    #           labels[11], labels[12], labels[0]]
    
    legend = ax.legend(handles, labels, loc="upper left",ncol=3,shadow=False,fancybox=True,framealpha = 0.0,fontsize=16)
    tick_params(axis='both', which='major', labelsize=22)
    legend.get_frame().set_facecolor('#DAEBF2')
    xlabel("$E_{\\rm{beam}}$ [MeV]", fontsize=22)
    ylabel("Cross-Section [mb]", fontsize=22)
    #ylim(0, 1e2)
    title("Relative Method", fontsize=22)
    show() 

    return '-------------------'
# ::::::::::::::::::::::::::::::::::::::::::::::: #