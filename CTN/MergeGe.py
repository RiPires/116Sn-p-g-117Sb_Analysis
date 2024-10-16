#RiP
####################################
from ReadData import *
import os
####################################

############################################################################
def MergeYieldGe(Dir):
    """
    Merges yields from different data .TXT files from Ge detector, 
    in a specific directory, into a single list
    INPUTS:
    directory containing data files
    OUTPUTS:
    Merged yield list
    """
    ConvYield = [0 for i in range(1024)]
    for file in os.listdir(Dir):
        Path = str(Dir+"\\"+file)
        Yield = Ge2Lists(Path)[0]
        ConvYield = [ConvYield[i] + Yield[i] for i in range(len(ConvYield))]
        
    return ConvYield