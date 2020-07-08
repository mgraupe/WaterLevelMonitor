import RPi.GPIO as GPIO
import time
from datetime import datetime
import numpy as np
import os
import sys
import pdb

import waterLevelScripts as waterLevel

try:
    sys.argv[1]
except:
    saveData = False
else:
    if sys.argv[1] == 'save':
        saveData = True
        print('Data will be saved.')
        print(saveData)

GPIO.setmode(GPIO.BOARD)

TRIG = 11
ECHO = 13
MaximalHeight = 95 # depth cannot be larger than this value

Nmeasurements = 50
verbose = True

scriptWD = os.path.dirname(os.path.realpath(__file__))


#################################################
def measurement():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(TRIG,0)

    GPIO.setup(ECHO,GPIO.IN)

    time.sleep(0.1)
    if verbose :
        print('starting measurement ...')

    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    dist = (stop-start)*17150
    if verbose:
        print('Distance is :',dist,' cm')
    return dist

###############################################

now = datetime.now()

depth = []
for i in range(Nmeasurements):
    d = measurement()
    depth.append(d)
    time.sleep(0.5)

GPIO.cleanup()

depth = np.asarray(depth)
depthClean = depth[depth<MaximalHeight]
currentDepth = np.median(depthClean)
currentH20Content = waterLevel.getWaterContentFromDistance(currentDepth,wd=scriptWD)
print('current water level : ',currentDepth,' cm')
print('current water content : ',currentH20Content,' l')
# write data to file

if saveData :
    dFile = open("%s/data/waterLevel2_%s.data" % (scriptWD,now.strftime("%Y-%m")),"a")
    dFile.write("%s %s\t%s\t%s\n" % (now.strftime("%Y-%m-%d"),now.strftime("%H:%M:%S"),np.round(currentDepth,3),np.round(currentH20Content,3)))
    dFile.close()
    print('data saved to file')
    
    print('plotting data ...')
    waterLevel.plotWaterLevel(wd=scriptWD)

###################################

