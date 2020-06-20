import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os 

def plotWaterLevel(wd=None):
    now = datetime.now()
    currentYearMonth = now.strftime("%Y-%m")


    wLevel = pd.read_csv(wd+'/data/waterLevel_%s.data' % currentYearMonth,sep='\t',header=None)

    #wLevel = pd.read_csv('/home/pi/WaterLevelMonitor/data/waterLevel_%s.data' % currentYearMonth,sep='\t',header=None)
    #print(wLevel.shape)
    #print(wLevel.head(3))
    #print(wLevel.tail(3))
    #wLevel.info()
    wLevel = wLevel.rename(columns={1:'WaterLevel'})
    wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H-%M-%S') 

    #ts = pd.Series(wLevel['Time'],wLevel[1])
    #ts.plot()
    wLevel.plot(x='Time',y='WaterLevel',style='.') 
    #plt.show()
    plt.savefig('%s/figures/waterLevel_%s.png' % (wd,currentYearMonth))
    os.system('cp %s/figures/waterLevel_%s.png %s/figures/waterLevel_current.png' % (wd,currentYearMonth,wd))
