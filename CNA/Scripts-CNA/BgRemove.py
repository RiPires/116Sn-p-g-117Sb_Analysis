############## RiP #################
## Script for removing background ##
####################################

## ---------------------------- ##
import os
from include.PlotData import *
from include.ReadData import *
from include.Merge import *
## ---------------------------- ##

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
def RemoveBg(dataFile):
    """
    Function that removes the background rate of an input dataFile, using the
    Backgroud measurement data. Writes out a new file with background removed.

    INPUTS: 
        - dataFile (str): path for data file; 
    """

    print('Removing background from file: ', dataFile)

    ## Check detector HPGe or SDD from file name
    if "HPGe" in dataFile:

        ## Set HPGe channels     
        ch = [(i+1) for i in range(4096)]

        ## Get run yield and acquisition live time   
        runYield, _, liveTime = Ge2Lists(dataFile)
        acquiTime = 15 * 60 # seconds = 15 minutes

        ## Background runs path
        bgPath = '../Calibrations/HPGe/Background/'

        ## Get background merged yield and time
        mergeBgYield, bgLiveTime = Merge(bgPath, 'ge')

        bgTime = 35*1800 + 777 ## seconds: 35 runs of 30 minutes each + 777 seconds for the last run

    elif "SDD" in dataFile:

        ## Set SDD channels
        ch = [(i+1) for i in range(2048)]

        ## Get run yield and acquisiton live time
        runYield, _, liveTime = MCA2Lists(dataFile)
        acquiTime = 30 * 60 # seconds = 30 minutes

        ## Background runs path
        bgPath = '../Calibrations/SDD/Background/'

        ## Get background merged yield and time
        mergeBgYield, bgLiveTime = Merge(bgPath, 'sdd')

        bgTime = 35*1800 + 777 ## seconds: 35 runs of 30 minutes each + 777 seconds for the last run
    
    print(f"\nData file time info.:")
    print(f"Real time = {acquiTime:.0f} s \nLive time = {liveTime:.0f} s \nDead time = {((acquiTime - liveTime)/acquiTime*100):.2f} %\n")
    print(f"Background time info.:")
    print(f"Real time  = {bgTime:.0f} s \nLive time = {bgLiveTime:.0f} s \nDead time = {((bgTime - bgLiveTime)/bgTime*100):.2f} %\n")

        
    ## Converts run yield into count rate (in s^-1)
    runRate = [runYield[i]/acquiTime for i in range(len(runYield))]

    ## Converts background yield into background count rate (in s^-1)
    bgRate = [mergeBgYield[i]/bgTime*(1-0.2794) for i in range(len(mergeBgYield))] # /(1 - 0.2794) is to correct for the dead time of 27.94%
    bgRateDTcorrect = [mergeBgYield[i]/bgTime*1.2794 for i in range(len(mergeBgYield))] # *1.2794 is to correct for the dead time of 27.94%

    ## Remove background rate from run data 
    runRateBgRem = [(runRate[i] - bgRate[i]) for i in range(len(runRate))]
    runRateBgRemDT = [(runRate[i] - bgRateDTcorrect[i]) for i in range(len(runRate))]

    ## Set labels
    lab = dataFile[-63:-51] + ': ' + dataFile[-12:-4]
    bgLab = 'Background Rate'
    bgDTLab = 'Background Rate (Dead Time Corrected)'
    rateLab = lab +'_BG removed'

    ## Plot both run data, bg rate and run data with bg removed 
    Plot3RateLogy(ch, runRate, runRateBgRem, runRateBgRemDT, lab, bgLab, bgDTLab)

    ## Save run rate with background removed values to file 
    """     with open(dataFile.replace(".mca","_BgRemoved.mca"), 'w') as outFile:
        counts = 0
        for rate in runRateBgRem:
            if rate <= 0:
                outFile.write(f"{counts:.0f}\n")
            elif rate > 0:
                counts = int(rate * acquiTime)      ## convert count rate back to counts
                outFile.write(f"{counts:.0f}\n")
    outFile.close() """

    return runRateBgRem, ch
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #


##  ***********************************************************  ##
##               Perform background removal here                 ##
##  ***********************************************************  ##

## Choose paths for data files
sddPaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_SDD/',
            '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/',]

gePaths = ['../Activations/Ebeam=3.2MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.5MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=3.9MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.3MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=4.7MeV/2_Decay/DataFiles_HPGe/',
           '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_HPGe/',]

 
## For each path, remove background for every data file
""" for path in gePaths:

    ## Prepare list to store removed background data
    bgRmYield = np.array([0. for i in range(4096)])
    for file in sorted(os.listdir(path)):
        bgRmRun, ch = RemoveBg(str(path+file))
        bgRmRun = np.array(bgRmRun)
        bgRmYield += bgRmRun
    print()

    fig, ax = plt.subplots()
    energy = np.array(ch)*0.3225 - 0.4556 # keV
    ax.semilogy(ch, bgRmYield, '+-', color='k', label='Bg Removed')
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('Energy [keV]',fontsize=22)
    xlim(left=0.)
    ylabel('CPS', fontsize=22)
    show() """

 
## For specific data file
filePath = '../Activations/Ebeam=5.0MeV/2_Decay/DataFiles_SDD/116Sn-D5_Decay_SDD_004.mca'
RemoveBg(filePath)