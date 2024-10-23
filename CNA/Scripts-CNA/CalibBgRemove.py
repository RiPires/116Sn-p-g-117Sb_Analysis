#################### RiP ###########################
## Script for removing background from the 152Eu  ##
## calibration run                                ##
####################################################

## ---------------------------- ##
from PlotData import *
from ReadData import *
from Merge import *
## ---------------------------- ##

##############################
## Get calibration run rate ##
##############################

## HPGe 152Eu Calibration run at 8mm det-source distance
calib152EuFile = '../Calibrations/HPGe/CalibrationRuns_PosExp/Run10_152Eu_detGe_8mm.mca'
## HPGe 152Eu Calibration yield at 8mm
calibYield = Ge2Lists(calib152EuFile)[0]
## Calibration acquisition time
calibTime = 900. # seconds
## Calib rate
calibRate = [calibYield[i]/calibTime for i in range(len(calibYield))]
## Set channel axes
ch_hpge = [((i+1)*0.3225-0.149) for i in range(4096)]
## Set label
lab = '152Eu - 8 mm'
## Plot calib rate
#PlotRateLogy(ch_hpge, calibRate, lab)

##############################
## Get background runs rate ##
##############################

## Background runs path
bgPath = '../Calibrations/HPGe/Background/'
## Merge background yield
mergeBgYield = Merge(bgPath, 'ge')
## Background acquisition time
bgTime = 35*1800 + 777 ## seconds: 35 runs * 1800 sec each + 777 sec last run
## Background rate
bgRate = [mergeBgYield[i]/bgTime for i in range(len(mergeBgYield))]
## Set label
bgLab = 'Background'
## Plot bg rate
#PlotRateLogy(ch_hpge, bgRate, bgLab)

##############################
## Plot both calib and bg rate
##############################
#PlotBothRateLogy(ch_hpge, calibRate, bgRate, lab, bgLab)

############################
## Remove background rate ##
############################

calibRateBgRem = [(calibRate[i] - bgRate[i]) for i in range(len(calibRate))]
## Set label
rateLab = '152Eu BG removed'
## Plot calib rate bg removed
#PlotRateLogy(ch_hpge, calibRateBgRem,rateLab)


########################################################
## Plot both calib, bg rate and calib with bg removed ##
########################################################
Plot3RateLogy(ch_hpge, calibRate, bgRate, calibRateBgRem, lab, bgLab, rateLab)