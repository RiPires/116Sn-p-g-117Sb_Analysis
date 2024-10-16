#################################################
## Fucntion to conver time format into a float ##
#################################################

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