####################### RiP ############################
## Functions to read data from different file formats ##
## and convert it to lists                            ##
########################################################

## ------------------------ ##
import csv
import os
from include.ConvTime2Float import *
## ------------------------ ##

#######################################################
#######################################################
def MCA2Lists(File):
    """
    Converts .mca data into yield and channel lists
    INPUTS:
        "FILENAME.mca"
    OUTPUTS:
        Yield and Channel lists
    HOW TO USE:
        MyYield, MyChannel = MCA2Lists("MyFile.mca")
    """
    with open(File, 'r', encoding='iso8859-4') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)

    ch = []
    y = []
    aux = []

    for i in range(2060):
        aux.append(data[i][0].split())

    ## Acquisition time    
    time = float(aux[7][2]) # seconds
    
    for i in range(12, len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch, time

#######################################################
#######################################################
def MCA2ListsBgRm(File):
    """
    Converts .mca data into yield and channel lists
    INPUTS:
        "FILENAME.mca"
    OUTPUTS:
        Yield and Channel lists
    HOW TO USE:
        MyYield, MyChannel = MCA2Lists("MyFile.mca")
    """
    with open(File, 'r',encoding='iso8859-4') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(2048):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch

#######################################################
#######################################################
def Ge2Lists(File):
    """
    Converts .dat data into yield and channel lists
    INPUTS:
        "FILENAME.mca"
    OUTPUTS:
        Yield and Channel lists
    HOW TO USE:
        MyYield, MyChannel = MCA2Lists("MyFile.mca")
    """
    with open(File, 'r', encoding='iso8859-4') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True, )
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(4110):
        aux.append(data[i][0].split())
    
    ## Acquisition time    
    time = float(aux[7][2])

    for i in range(14, len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch, time

#######################################################
#######################################################
def Ge2ListsBgRm(File):
    """
    Converts .dat data into yield and channel lists
    INPUTS:
        "FILENAME.mca"
    OUTPUTS:
        Yield and Channel lists
    HOW TO USE:
        MyYield, MyChannel = MCA2Lists("MyFile.mca")
    """
    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True, )
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(4096):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch

#######################################################
#######################################################
def ReadActivationRBS(File):

    ch = []
    cts = []
    aux = []

    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter='\n', skipinitialspace=True)
        data = list(reader)

    for i in range(1, len(data)):
        aux.append(data[i][0].split())

    for i in range(len(aux)):
        ch.append(int(aux[i][0]) + 1)
        cts.append(float(aux[i][1]))

    return ch, cts

#######################################################
#######################################################
def ReadCurrent(iPath):

    time = []
    current = []
    aux = []

    for File in os.listdir(iPath):

        with open(str(iPath+File), 'r') as file:
            reader = csv.reader(file, delimiter='\n', skipinitialspace=True)
            data = list(reader)

        for i in range(len(data)):
            aux.append(data[i][0].split())
        for i in range(len(aux)):
            time.append(float(conv_time_float(aux[i][0])))
            current.append(float(aux[i][2]))
    
    return time, current