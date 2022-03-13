import sys
import os
from datetime import datetime
import numpy as np
import time
from ISStreamer.Streamer import Streamer

import bme280
import ds18b20
import jsn_sr0t4_2
import scrapeRainfall

import ITaccess as ITA

SENSOR_LOCATION_NAME = "My Terrace"

def main(saveData,now,scriptWD):

    bme = bme280.bme280()
    (temperature,pressure,humidity) = bme.readBME280All()
    print("Temperature : ", temperature, "C")
    print("Pressure : ", pressure, "hPa")
    print("Humidity : ", humidity, "%")
    del bme

    ds = ds18b20.ds18b20()
    temp_c = ds.readDS18b20All()
    for n in range(len(temp_c)):
        print("Senor # : ", n)
        print("Sensor ID : ", temp_c[n][1])
        print("Sensor name :", temp_c[n][2])
        print("Temperature : ", temp_c[n][3], "C")
        if temp_c[n][2] == 'Water bucket':
            tempInBucket = temp_c[n][3]
    del ds

    jsn = jsn_sr0t4_2.jsnsr0t4(tempInBucket)
    (currentDepth, currentH20Content) = jsn.readJSNSR0T4()
    print('current water level : ', currentDepth, ' cm')
    print('current water content : ', currentH20Content, ' l')
    del jsn

    time.sleep(1.) # wait a second for the read LED to switch off
    import tsl2591 # has to be imported here, otherwise jsn_sr0t4 script gives error
    tsl = tsl2591.tsl2591()
    (lux,infrared,visible,full_spectrum) = tsl.readTSL2591All()
    print("Total light : ", lux, "lux")
    print("Infrared light : ", infrared)
    print("Visible light : ", visible)
    print("Full spectrum (IR + visible) light : ", full_spectrum)
    del tsl

    minutes = int(now.strftime("%M"))
    rainfallScraped = False
    if (minutes > 19) and (minutes < 29): # scrape rainfall only once per hour at 20 min
        fullHour = now.strftime("%Hh00")
        rf = scrapeRainfall.scrapeRainfall(fullHour)
        (pluie, hour) = rf.getRainfallData()
        print("Measurement hour :", hour)
        print("Rainfall in mm   :", pluie)

        waterChange = rf.getDifferenceInWaterButtContent(now)
        print("Water in butt changed by : %s l between %02dh and %02dh" % (waterChange[0],waterChange[1],waterChange[2]))
        rainfallScraped = True


    if saveData:
        dFile = open("%s/data/terraceWeather_%s.data" % (scriptWD, now.strftime("%Y-%m")), "a")
        dFile.write("%s %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), temperature,np.round(pressure, 2),np.round(humidity, 2),temp_c[0][3],temp_c[1][3],np.round(currentDepth, 3), np.round(currentH20Content, 3),np.round(lux,4),infrared,visible,full_spectrum))
        dFile.close()
        print('data saved to file')

        # send data to initial state
        streamer = Streamer(bucket_name=ITA.BUCKET_NAME, bucket_key=ITA.BUCKET_KEY, access_key=ITA.ACCESS_KEY)
        #print(np.round(humidity, 2),np.round(pressure, 2),temperature,temp_c[0][3],temp_c[1][3],np.round(currentH20Content, 3),np.round(lux,4))
        streamer.log(SENSOR_LOCATION_NAME + " Humidity (%)", np.float(np.round(humidity, 2)))
        streamer.log(SENSOR_LOCATION_NAME + " Pressure (hPa)", np.round(pressure, 2))
        streamer.log(SENSOR_LOCATION_NAME + " Chip Temperature (C)", temperature)
        streamer.log(SENSOR_LOCATION_NAME + " Water Bucket Temperature (C)", temp_c[0][3])
        streamer.log(SENSOR_LOCATION_NAME + " Outside Temperature (C)", temp_c[1][3])
        streamer.log(SENSOR_LOCATION_NAME + " Water Content (l)", np.round(currentH20Content, 3))
        streamer.log(SENSOR_LOCATION_NAME + " Luminosity (lux)", np.round(lux,4))
        if rainfallScraped:
            if pluie is not None:
                streamer.log(SENSOR_LOCATION_NAME + " Rainfall (mm)", pluie)
            streamer.log(SENSOR_LOCATION_NAME + " Water Change (l)", np.round(waterChange[0],4))

            dFile = open("%s/data/rainfallWaterChange_%s.data" % (scriptWD,now.strftime("%Y-%m")),"a")
            dFile.write("%s %s\t%s\t%s\n" % (now.strftime("%Y-%m-%d"),now.strftime("%H:00"),pluie,np.round(waterChange[0],4)))
            dFile.close()
            print('rainfall and water change data saved to file')

        streamer.flush()
        print('Upload code finished')

        #print('plotting data ...')
        #waterLevel.plotWaterLevel(wd=scriptWD)

        #print('plotting rainfall data ...')
        #waterLevel.plotRainFallData(wd=scriptWD)

if __name__=="__main__":
    try:
        sys.argv[1]
    except:
        saveData = False
    else:
        if sys.argv[1] == 'save':
            saveData = True
            print('Data will be saved.')
            print(saveData)
    now = datetime.now()
    print('run at %s' % now.strftime("%Y-%m-%d %H:%M:%S"))
    scriptWD = os.path.dirname(os.path.realpath(__file__))
    main(saveData,now,scriptWD)
