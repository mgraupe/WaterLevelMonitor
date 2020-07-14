import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os 
import numpy as np
from scipy.interpolate import interp1d
import pdb

####################################################################################
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
    wLevel.plot(x='Time',y='DistanceToWater',style='_',ms=1,ax=plt.gca(),label='last dist.=%s cm' % np.round(wLevel['DistanceToWater'].iloc[-1],1)) 
    plt.ylabel('distance to water surface (cm)',fontsize=14)
    plt.xlabel('date and time',fontsize=14)
    #plt.show()
    plt.subplot(212)
    wLevel.plot(x='Time',y='WaterContent',style='_',ms=1,ax=plt.gca(),label='cur. content=%s l' % np.round(wLevel['WaterContent'].iloc[-1],2)) 
    plt.ylabel('water content (l)',fontsize=14)
    plt.xlabel('date and time',fontsize=14)
    #
    plt.savefig('%s/figures/waterLevel_%s.png' % (wd,currentYearMonth))
    os.system('cp %s/figures/waterLevel_%s.png %s/figures/waterLevel_current.png' % (wd,currentYearMonth,wd))

####################################################################################
def plotRainFallData(wd=None):
    now = datetime.now()
    currentYearMonth = now.strftime("%Y-%m")


    wLevel = pd.read_csv(wd+'/data/terraceWeather_%s.data' % currentYearMonth,sep='\t',header=None)
    rainfall = pd.read_csv(wd+'/data/rainfall_%s.data' % currentYearMonth,sep='\t',header=None)

    #wLevel = pd.read_csv('/home/pi/WaterLevelMonitor/data/waterLevel_%s.data' % currentYearMonth,sep='\t',header=None)
    #print(wLevel.shape)
    #print(wLevel.head(3))
    #print(wLevel.tail(3))
    #wLevel.info()

    wLevel = wLevel.rename(columns={6:'DistanceToWater'})
    wLevel = wLevel.rename(columns={7:'WaterContent'})
    wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H:%M:%S') 
    wLevel = wLevel.set_index('Time')
    wLevel.drop([0], axis=1, inplace=True)
    #wLevelFullHour = wLevel.resample('H').first()
    #increases = np.diff(wLevelFullHour['WaterContent'])
    
    #wLevelSummary = pd.DataFrame()
    wLevelSummary = wLevel.resample('H').first()
    wLevelSummary['Change'] = np.hstack((0,np.diff(wLevelSummary['WaterContent'])))
    #wLevelSummary = wLevelSummary.drop(['DistanceToWater','WaterContent'],axis=1)
    
    rainfall = rainfall.rename(columns={1:'Rainfall'})
    rainfall['Time'] = pd.to_datetime(rainfall[0], format='%Y-%m-%d %H:%M') 
    rainfall = rainfall.set_index('Time')
    rainfall.drop([0], axis=1, inplace=True)
    
    joinedTS = wLevelSummary.join(rainfall)
    mask = joinedTS['Rainfall']>0.

    #pdb.set_trace()
    
    #ts = pd.Series(wLevel['Time'],wLevel[1])
    #ts.plot()
    plt.figure(figsize=(7,10))
    plt.subplots_adjust(left=0.15, right=0.88, top=0.95, bottom=0.1,hspace=0.4)
    ax0 = plt.subplot(211)
    #fig, axes = plt.subplots(nrows=2, ncols=1)
    joinedTS.plot(y='Rainfall',style='_',ms=5,ax=ax0)#,style='_',ms=2,ax=ax0) 
    joinedTS.plot(y='Change',secondary_y=True,style='_',ms=5,ax=ax0)
    #ax1 = ax0.twinx()
    #wLevelSummary.plot(y='Change',secondary_y=True,style='_',ms=2,ax=ax0) 
    
    ax0.set_ylabel('Rainfall (mm/1h)',fontsize=14)
    ax0.right_ax.set_ylabel('Positive water change (l)',fontsize=14)
    ax0.right_ax.set_ylim(-1,)
    ax0.set_xlabel('date and time',fontsize=14)
    #ax0.set_xlim(pd.Timestamp('2020-07-01'), pd.Timestamp('2020-07-10'))
    #plt.show()
    if sum(mask)>0:
        ax1 = plt.subplot(212)
        wLevel[mask].plot(x='Rainfall',y='Change',style='*',ms=1,ax=ax1) 
        ax1.set_ylabel('Water change (l)',fontsize=14)
        ax1.set_xlabel('Rainfall (mm/1h)',fontsize=14)
    #
    plt.savefig('%s/figures/rainfall_%s.png' % (wd,currentYearMonth))
    os.system('cp %s/figures/rainfall_%s.png %s/figures/rainfall_current.png' % (wd,currentYearMonth,wd))

####################################################################################
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
    
