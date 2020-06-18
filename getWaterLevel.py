import RPi.GPIO as GPIO
import time
from datetime import datetime
import numpy as np
import os


GPIO.setmode(GPIO.BOARD)

TRIG = 11
ECHO = 13
MaximalHeight = 95 # depth cannot be larger than this value


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
Nmeasurements = 50
verbose = True


now = datetime.now()

depth = []
for i in range(Nmeasurements):
    d = measurement()
    depth.append(d)
    time.sleep(0.5)

depth = np.asarray(depth)
depthClean = depth[depth<MaximalHeight]
currentDepth = np.median(depthClean)
print('actual water level : ',currentDepth,' cm')
# write data to file
cwd = os.getcwd()

dFile = open(cwd+"/data/waterLevel_%s.data" % now.strftime("%Y-%m"),"a")
dFile.write("%s %s %s\n" % (now.strftime("%Y-%m-%d"),now.strftime("%H-%M-%S"),currentDepth))
dFile.close()

GPIO.cleanup()

