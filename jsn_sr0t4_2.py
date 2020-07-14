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


class jsnsr0t4:
    def __init__(self):
        
        self.TRIG = 11
        self.ECHO = 13
        self.MaximalHeight = 95 # depth cannot be larger than this value
        self.Nmeasurements = 50 # number of measurements, final value is median, measurements are noisy
        self.verbose = True
        #GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

    def measurement(self):

        GPIO.setup(self.TRIG,GPIO.OUT)
        GPIO.setup(self.TRIG,0)

        GPIO.setup(self.ECHO,GPIO.IN)

        time.sleep(0.1)
        if self.verbose :
            print('starting measurement ...')

        GPIO.output(self.TRIG,1)
        time.sleep(0.00001)
        GPIO.output(self.TRIG,0)

        while GPIO.input(self.ECHO) == 0:
            pass
        start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pass
        stop = time.time()

        dist = (stop-start)*17150
        if self.verbose:
            print('Distance is :',dist,' cm')
        return dist

    def readJSNSR0T4(self):
        #GPIO.cleanup()
        #GPIO.setmode(GPIO.BOARD)

        depth = []
        for i in range(self.Nmeasurements):
            d = self.measurement()
            depth.append(d)
            time.sleep(0.5)

        GPIO.cleanup()

        depth = np.asarray(depth)
        depthClean = depth[depth<self.MaximalHeight]
        currentDepth = np.median(depthClean)
        scriptWD = os.path.dirname(os.path.realpath(__file__))
        currentH20Content = waterLevel.getWaterContentFromDistance(currentDepth,wd=scriptWD)

        return(currentDepth,currentH20Content)

def main():

    jsn = jsnsr0t4()
    (currentDepth, currentH20Content) = jsn.readJSNSR0T4()

    print('current water level : ', currentDepth, ' cm')
    print('current water content : ', currentH20Content, ' l')


if __name__=="__main__":
    main()




