#import requests
#import xml.etree.ElementTree as ET
import pandas as pd
import pdb
from datetime import datetime
import os

now = datetime.now()
fullHour = now.strftime("%Hh00")
saveData = True
scriptWD = os.path.dirname(os.path.realpath(__file__))

# scrape tables from infoclimat website
url = r'https://www.infoclimat.fr/observations-meteo/temps-reel/paris-6eme-saint-germain-des-pres/000CT.html'
tables = pd.read_html(url) # Returns list of all tables on page
weatherValues = tables[1] # Select table of interest

n = 0
while True:
    hour  = tables[1]['Heure locale'][n]
    #print(hour, fullHour)
    if hour == fullHour:
        pluie = float(weatherValues['Pluie'][n].split()[0])
        break
    n+=1
    
print('It rained %s mm in the last hour : %s' %(pluie,hour))
    

if saveData :
    dFile = open("%s/data/rainfall_%s.data" % (scriptWD,now.strftime("%Y-%m")),"a")
    dFile.write("%s %s\t%s\n" % (now.strftime("%Y-%m-%d"),now.strftime("%H:00"),pluie))
    dFile.close()
    print('rainfall data saved to file')



