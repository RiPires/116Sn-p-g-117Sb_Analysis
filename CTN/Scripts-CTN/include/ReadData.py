########################################################
## Functions to read data from different file formats ##
## and convert it to lists                            ##
########################################################

## ------------------------ ##
import csv
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
    Converts .TXT ASCii data into yield and channel lists
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
    for i in range(1, 1025):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))

    return y, ch

#######################################################
#######################################################
def Read_TANDEM_RBS_Data(data, det):

    Data_x = []
    Data_y = []
    aux = []

    if det == 1:
        for i in range(143, 142+1024):
            aux.append(data[i][0].split())
    elif det == 2:
        for i in range(1167, 1167+1024):
            aux.append(data[i][0].split())
    elif det == 3:
        for i in range(2191, 2191+1024):
            aux.append(data[i][0].split())
    elif det == 4:
        for i in range(3215, len(data)-1):
            aux.append(data[i][0].split())

    for i in range(len(aux)):
        Data_x.append(float(i)) ## axes in channel
        Data_y.append(float(aux[i][0]))

    return Data_x, Data_y

#######################################################
#######################################################
def ReadActivationRBS(data, det):
    Data_x = []
    Data_y = []
    aux = []

    if det == 1:
        for i in range(1, 1025):
            aux.append(data[i][0].split())
    elif det == 3:
        for i in range(1026, 1026+8192):
            aux.append(data[i][0].split())
    elif det == 4:
        for i in range(9219, len(data)-1):
            aux.append(data[i][0].split())

    for i in range(len(aux)):
        Data_x.append(float(i)) ## axes in channel
        Data_y.append(float(aux[i][0]))

    return Data_x, Data_y

#######################################################
#######################################################
def ReadCurrent(file):

    time = []
    current = []
    aux = []

    with open(str(file), 'r') as file:
        reader = csv.reader(file, delimiter='\n', skipinitialspace=True)
        data = list(reader)

    for i in range(len(data)):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        time.append(float(aux[i][0]))
        current.append(float(aux[i][1]))

    return time, current