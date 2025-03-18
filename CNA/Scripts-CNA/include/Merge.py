########################  RiP  #######################
## Script for merging data file from different runs ##
######################################################

## ---------------------------- ##
import os
from include.ReadData import*
## ---------------------------- ##

def Merge(dir, det):
    """
    Merges data from different runs into a single yield

    INPUTS:
            dir: path to the directory containing the data files to merge
            det: which detector is being used - either ge or sdd
    OUPUTS:
            array of merged yield
    """
    
    ## Check which detector is being used
    if det == 'ge':
        nrCh = int(4096)
    elif det == 'sdd':
        nrCh = int(2048)
    else:
        print('Detector not recognized')
    
    ## Set up array of zeros for merge yield depending on the detector
    mergeYield = [0 for i in range(nrCh)]
    totTime_sec = 0.

    ## Loop over the data files and merge yield
    for file in os.listdir(dir):

        if det == 'ge':
            y = Ge2Lists(str(dir+file))[0]

        elif det == 'sdd':
            y, _, runTime = MCA2Lists(str(dir+file))

        mergeYield = [mergeYield[i] + y[i] for i in range(len(y))]
        totTime_sec += runTime # seconds

    return mergeYield, totTime_sec

def MergeAndRate(dir, totTime):
    """
    Merges data from different runs of the Ge detector 
    into a single yield, dividing by the total acquisition 
    time to get accumulated rate

    INPUTS:
            dir: path to the directory containing the data files to merge
            totTime: total acquisition time
    OUPUTS:
            array of merged rate
    """

    ## set up array of zeros for merge rate
    mergeYield = [0 for i in range(4096)]

    ## loop over the datafiles and merge yield
    for file in os.listdir(dir):
        y = Ge2Lists(str(dir+file))[0]
        mergeYield = [mergeYield[i] + y[i] for i in range(len(y))]

    mergeRate = [mergeYield[i]/totTime for i in range(len(mergeYield))] ## s-1
    
    return mergeRate