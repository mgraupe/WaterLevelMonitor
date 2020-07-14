import sys
import os
from datetime import datetime

import bme280
import tsl2591
import ds18b20
import jsn_sr0t4_2

def main(saveData,now,scriptWD):

    (temperature,pressure,humidity) = bme280.readBME280All()
    print("Temperature : ", temperature, "C")
    print("Pressure : ", pressure, "hPa")
    print("Humidity : ", humidity, "%")

    (lux,infrared,visible,full_spectrum) = tsl2591.readTSL2591All()
    print("Total light : ", lux, "lux")
    print("Infrared light : ", infrared)
    print("Visible light : ", visible)
    print("Full spectrum (IR + visible) light : ", full_spectrum)

    temp_c = ds18b20.readDS18b20All()
    for n in range(len(temp_c)):
        print("Senor # : ", n)
        print("Sensor ID : ", temp_c[n][1])
        print("Sensor name :", temp_c[n][2])
        print("Temperature : ", temp_c[n][3], "C")

    (currentDepth, currentH20Content) = jsn_sr0t4_2.readJSNSR0T4()
    print('current water level : ', currentDepth, ' cm')
    print('current water content : ', currentH20Content, ' l')

    if saveData:
        dFile = open("%s/data/terraceWeather_%s.data" % (scriptWD, now.strftime("%Y-%m")), "a")
        dFile.write("%s %s\t%s\t%s\n" % (now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), np.round(currentDepth, 3), np.round(currentH20Content, 3)))
        dFile.close()
        print('data saved to file')

        #print('plotting data ...')
        #waterLevel.plotWaterLevel(wd=scriptWD)

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
    scriptWD = os.path.dirname(os.path.realpath(__file__))
    main(saveData,now,scriptWD)
