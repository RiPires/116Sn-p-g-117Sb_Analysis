#################################################
## Fucntion to conver time format into a float ##
#################################################

## *********************************************** ##
def conv_time_float(value):
    """
    Converts a value of time in the format HH:MM:SS to a float of seconds.
    It is used to conver the time values of the current monitor data.
    
    INPUTS: value - time in format HH:MM:SS

    OUPUTS: time float in seconds since 00h00
    """
    vals = value.split(':')

    hours = int(vals[0])
    min = int(vals[1])
    sec = int(vals[2])

    ## return nr of seconds since 00h00
    return float(hours*3600 + min*60 + sec)
## *********************************************** ##

## *********************************************** ##
def time2FLoatIrrad(tValue, irradStart):
    """
    Converts a value of time, in the format HH:MM:SS, to a float as the number of seconds
    since the begining of the activation.

    INPUTS: tValue - time in the format HH::MM:SS
            irradStart - time, in the format HH:M:SS, when the irradiation begun;

    OUTPUTS: time float in seconds since the begining of the activation
    """

    tValue = conv_time_float(tValue)
    irradStart = conv_time_float(irradStart)

    ## return nr of seconds since the begining of the activation
    return float(tValue - irradStart)
## *********************************************** ##
