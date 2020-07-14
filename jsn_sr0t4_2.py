#   JSN-SR0T4-2.0 ultrasonic distance sensor
#   prints distance to water surface in water bucket
#   converts distance in water content

import RPi.GPIO as GPIO
import time
import numpy as np
import os
import sys
import pdb

import waterLevelScripts as waterLevel

TRIG = 11
ECHO = 13
MaximalHeight = 95 # depth cannot be larger than this value
Nmeasurements = 50 # number of measurements, final value is median, measurements are noisy
verbose = True

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

def readJSNSR0T4():
    GPIO.setmode(GPIO.BOARD)

    depth = []
    for i in range(Nmeasurements):
        d = measurement()
        depth.append(d)
        time.sleep(0.5)

    GPIO.cleanup()

    depth = np.asarray(depth)
    depthClean = depth[depth<MaximalHeight]
    currentDepth = np.median(depthClean)
    scriptWD = os.path.dirname(os.path.realpath(__file__))
    currentH20Content = waterLevel.getWaterContentFromDistance(currentDepth,wd=scriptWD)

    return(currentDepth,currentH20Content)

def main():

    (currentDepth, currentH20Content) = readJSNSR0T4()

    print('current water level : ', currentDepth, ' cm')
    print('current water content : ', currentH20Content, ' l')


if __name__=="__main__":
    main()




