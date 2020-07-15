###########################################
# TSL2591 sensor
# will print the detected light value
###########################################
import time

import board
import busio

import adafruit_tsl2591


class tsl2591:
    def __init__(self):
        # Initialize the I2C bus.
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize the sensor.
        self.sensor = adafruit_tsl2591.TSL2591(self.i2c)
        self.sensor.enable()
    def readTSL2591All(self):


        # You can optionally change the gain and integration time:
        #self.sensor.gain = adafruit_tsl2591.GAIN_LOW #(1x gain)
        self.sensor.gain = adafruit_tsl2591.GAIN_MED #(25x gain, the default)
        # sensor.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
        # sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
        #self.sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS #(100ms, default)
        self.sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS #(200ms)
        # sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
        # sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
        # sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
        # sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)

        # Read the total lux, IR, and visible light levels and print it every second.
        #while True:
        #for n in range(Nmeasurements):
        # Read and calculate the light level in lux.
        lux = self.sensor.lux
        #print("Total light: {0}lux".format(lux))
        # You can also read the raw infrared and visible light levels.
        # These are unsigned, the higher the number the more light of that type.
        # There are no units like lux.
        # Infrared levels range from 0-65535 (16-bit)
        infrared = self.sensor.infrared
        #print("Infrared light: {0}".format(infrared))
        # Visible-only levels range from 0-2147483647 (32-bit)
        visible = self.sensor.visible
        #print("Visible light: {0}".format(visible))
        # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
        full_spectrum = self.sensor.full_spectrum
        #print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
        #self.sensor.disable()
        #self.i2c.deinit()
        return (lux,infrared,visible,full_spectrum)
        #time.sleep(1.0)

def main():

    tsl = tsl2591()

    (lux,infrared,visible,full_spectrum) = tsl.readTSL2591All()
    del tsl

    print("Total light : ", lux, "lux")
    print("Infrared light : ", infrared)
    print("Visible light : ", visible)
    print("Full spectrum (IR + visible) light : ", full_spectrum)

if __name__=="__main__":
    main()