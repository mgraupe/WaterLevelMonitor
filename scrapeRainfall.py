#import requests
#import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import pdb
from datetime import datetime
import os
import sys

import waterLevelScripts as waterLevel


class scrapeRainfall:
    def __init__(self,fullH):
        #now = datetime.now()
        self.fullHour = fullH #now.strftime("%Hh00")
        self.scriptWD = os.path.dirname(os.path.realpath(__file__))
        self.nMaxRows = 12

    def getRainfallData(self):
        # scrape tables from infoclimat website
        # water fall data is from weather station : Paris 6ème - Saint Germain des Prés
        # Département 75 Paris
        # Altitude 60 mètres
        # Coordonnées 48,85°N | 2,34°E
        url = r'https://www.infoclimat.fr/observations-meteo/temps-reel/paris-6eme-saint-germain-des-pres/000CT.html'
        tables = pd.read_html(url) # Returns list of all tables on page
        weatherValues = tables[1] # Select table with weather data

        n = 0
        measurementExists = False
        while n<self.nMaxRows:
            hour  = tables[1]['Heure locale'][n]
            #print(hour, fullHour)
            if hour == self.fullHour:
                pluie = float(weatherValues['Pluie'][n].split()[0])
                measurementExists = True
                break
            n+=1

        if measurementExists:
            print('It rained %s mm in the last hour : %sh' %(pluie,hour))
            return (pluie,hour)
        else:
            print('Rainfall data not available for last hour : %sh ' % hour)
            return (None,hour)
    
    def getDifferenceInWaterButtContent(self,now,fullH=None):
        if fullH is None:
            fullHourInt = int(now.strftime("%H"))
        else:
            fullHourInt = fullH
        date = now.strftime("%Y-%m-%d")
        currentYearMonth = now.strftime("%Y-%m")
        wLevel = pd.read_csv(self.scriptWD+'/data/terraceWeather_%s.data' % currentYearMonth,sep='\t',header=None)
        wLevel = wLevel.rename(columns={6:'DistanceToWater'})
        wLevel = wLevel.rename(columns={7:'WaterContent'})
        wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H:%M:%S')
        wLevel = wLevel.set_index('Time')
        wLevel.drop([0], axis=1, inplace=True)


        wLevelSummary = wLevel.resample('H').first() # resample weather-data to 1 hour interval, use the first value of each hour after resampling
        wLevelSummary['Change'] = np.hstack((0,np.diff(wLevelSummary['WaterContent'])))

        currentH = wLevelSummary[date].between_time(start_time='%02d:50' % (fullHourInt-1),end_time='%02d:10' % fullHourInt)['Change']
        #pdb.set_trace()
        if len(currentH)==0:
            print('None')
        else:
            return (currentH[0])
        #pdb.set_trace()

def main():

    now = datetime.now()
    fullHour = now.strftime("%Hh00")

    rf = scrapeRainfall(fullHour)
    (pluie, hour) = rf.getRainfallData()
    print("Measurement hour :", hour)
    print("Rainfall in mm   :", pluie)

    (waterChange) = rf.getDifferenceInWaterButtContent(now)
    print("Water in butt changed by : %s l between %02dh and %02dh" % (waterChange,int(now.strftime("%H"))-1,int(now.strftime("%H"))))


if __name__=="__main__":
    main()
