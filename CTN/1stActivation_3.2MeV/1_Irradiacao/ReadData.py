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
