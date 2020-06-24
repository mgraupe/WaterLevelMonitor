import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os 
import numpy as np
from scipy.interpolate import interp1d
import pdb

def plotWaterLevel(wd=None):
    now = datetime.now()
    currentYearMonth = now.strftime("%Y-%m")


    wLevel = pd.read_csv(wd+'/data/waterLevel2_%s.data' % currentYearMonth,sep='\t',header=None)

    #wLevel = pd.read_csv('/home/pi/WaterLevelMonitor/data/waterLevel_%s.data' % currentYearMonth,sep='\t',header=None)
    #print(wLevel.shape)
    #print(wLevel.head(3))
    #print(wLevel.tail(3))
    #wLevel.info()

    wLevel = wLevel.rename(columns={1:'DistanceToWater'})
    wLevel = wLevel.rename(columns={2:'WaterContent'})
    wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H:%M:%S') 
    
    #pdb.set_trace()

    #ts = pd.Series(wLevel['Time'],wLevel[1])
    #ts.plot()
    plt.figure(figsize=(6,10))
    plt.subplots_adjust(left=0.2, right=0.96, top=0.95, bottom=0.1,hspace=0.4)
    plt.subplot(211)
    #fig, axes = plt.subplots(nrows=2, ncols=1)
    wLevel.plot(x='Time',y='DistanceToWater',style='_',ms=1,ax=plt.gca()) 
    plt.ylabel('distance to water surface (cm)',fontsize=14)
    plt.xlabel('date and time',fontsize=14)
    #plt.show()
    plt.subplot(212)
    wLevel.plot(x='Time',y='WaterContent',style='_',ms=1,ax=plt.gca()) 
    plt.ylabel('water content (l)',fontsize=14)
    plt.xlabel('date and time',fontsize=14)
    #
    plt.savefig('%s/figures/waterLevel_%s.png' % (wd,currentYearMonth))
    os.system('cp %s/figures/waterLevel_%s.png %s/figures/waterLevel_current.png' % (wd,currentYearMonth,wd))


def getWaterContentFromDistance(dist,wd=None):
    calData = np.load(wd+'/data/calibrationData.npy')
    H20interp = interp1d(calData[:,1], calData[:,0])
    if dist > calData[0,1]:
        H20 = 0.
    elif dist < calData[-1,1]:
        H20 = calData[-1,0]
    else:
        H20 = H20interp(dist)
    return H20
    
