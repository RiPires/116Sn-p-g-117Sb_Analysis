#RiP

###   Normalization function   ###
def Normalize(data):
    """
    Normalizes a list to it's max. value
    returns a new list 
    """
    norm_data = []
    for entrie in data:
        norm_data.append(entrie/max(data))
    return norm_data