#RiP
import csv

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
    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(12, 2060):
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
    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(14, 4110):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch