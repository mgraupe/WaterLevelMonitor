###########################################
# DS18B20 temperature sensor
# will print temperature of all connected probes
###########################################
import os
import glob
import time
import pdb
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
device_names = ['Water bucket','Outside Terrace']
#device_file = device_folder + '/w1_slave'
 
def read_temp_raw(dev_file):
    f = open(dev_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def readDS18b20All():
    temp_c = []
    for n in range(len(device_folders)):
        dev_file = device_folders[n] + '/w1_slave'
        lines = read_temp_raw(dev_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_c.append([n,device_folders[n],device_names[n],temp])
    return temp_c
	
#while True:
#	print(read_temp())
#	time.sleep(1)
def main():

    temp_c = readDS18b20All()
    for n in range(len(temp_c)):
        print("Senor # : ", n)
        print("Sensor ID : ", temp_c[n][1])
        print("Sensor name :", temp_c[n][2])
        print("Temperature : ", temp_c[n][3], "C")

if __name__=="__main__":
    main()