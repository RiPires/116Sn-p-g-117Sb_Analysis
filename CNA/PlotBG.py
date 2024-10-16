#################### RiP #########################
## Script for plotting detector background runs ##
##################################################

## ---------------------------- ##
from PlotData import *
from ReadData import *
from Merge import *
## ---------------------------- ##

## Set channel axes
ch_hpge = [((i+1)*0.3225-0.149) for i in range(4096)]
ch_sdd = [(i+1) for i in range(2048)]

## HPGe backgroubd runs path
bgPathHPGe = 'Calibrations/HPGe/Background/'
## Merge HPGe background runs
mergeYieldHPGe = Merge(bgPathHPGe, 'ge')
## Plot merged yield HPGe
lab_hpge = 'HPGe background'
PlotLogy(ch_hpge, mergeYieldHPGe, str(lab_hpge))

## SDD background runs path
bgPathSDD =  'Calibrations/SDD/Background/'
## Merge SDD background runs
mergeYieldSDD = Merge(bgPathSDD, 'sdd')
## Plot merged yield SDD
lab_sdd = 'SDD background'
Plot(ch_sdd, mergeYieldSDD, str(lab_sdd))