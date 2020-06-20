import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os 
import numpy as np
from scipy.interpolate import interp1d

def plotWaterLevel(wd=None):
    now = datetime.now()
    currentYearMonth = now.strftime("%Y-%m")


    wLevel = pd.read_csv(wd+'/data/waterLevel2_%s.data' % currentYearMonth,sep='\t',header=None)

    #wLevel = pd.read_csv('/home/pi/WaterLevelMonitor/data/waterLevel_%s.data' % currentYearMonth,sep='\t',header=None)
    #print(wLevel.shape)
    #print(wLevel.head(3))
    #print(wLevel.tail(3))
    #wLevel.info()
    wLevel = wLevel.rename(columns={1:'WaterLevel'})
    wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H:%M:%S') 

    #ts = pd.Series(wLevel['Time'],wLevel[1])
    #ts.plot()
    wLevel.plot(x='Time',y='WaterLevel',style='.') 
    #plt.show()
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
    
