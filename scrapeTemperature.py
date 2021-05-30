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
    def __init__(self):
        #now = datetime.now()
        #self.fullHour = fullH #now.strftime("%Hh00")
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
        #pdb.set_trace()
        timeKey = [y for y in weatherValues.keys() if 'Heure locale' in y]
        tempKey = [y for y in weatherValues.keys() if 'Température' in y]
        #pdb.set_trace()
        n = 0
        measurementExists = False
        while n<self.nMaxRows:
            hour  = weatherValues[timeKey[0]][n]
            temp = float(weatherValues[tempKey[0]][n].split()[0])
            if (hour is not None) and (temp is not None):
                measurementExists = True
                break
            n+=1

        if measurementExists:
            print('The temperature is %s °C at  %s' %(temp,hour))
            return (temp,hour)
        else:
            print('Temperature data not available for time %s ' % hour)
            return (None,hour)
    

def main():

    now = datetime.now()
    currentTime = now.strftime("%Hh%M")
    currentTimeDTO = datetime.strptime(currentTime,'%Hh%M')
    
    rf = scrapeRainfall()
    (temp, hour) = rf.getRainfallData()
    hourDTO = datetime.strptime(hour,'%Hh%M')
    print("current time :", currentTime)
    print("Measurement time  :", hour)
    print("Temperature in °C :", temp)
    diffTime = (currentTimeDTO-hourDTO).total_seconds() /60
    print(diffTime)

    #(waterChange,hourBefore,currentHour) = rf.getDifferenceInWaterButtContent(now)
    #print("Water in butt changed by : %s l between %02dh and %02dh" % (waterChange,hourBefore,currentHour))


if __name__=="__main__":
    main()
