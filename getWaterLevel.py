import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 11
ECHO = 13

def measurement():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(TRIG,0)

    GPIO.setup(ECHO,GPIO.IN)

    time.sleep(0.1)

    print('starting measurement ...')

    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    dist = (stop-start)*17150

    print('Distance is :',dist,' cm')



while True:
    measurement()
    time.sleep(0.5)
    
GPIO.cleanup()

