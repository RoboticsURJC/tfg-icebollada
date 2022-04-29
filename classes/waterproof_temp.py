import os
import glob
import time

class DS18B20:
    def __init__(self):
        self.temp = 0
        #these two lines mount the device:
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.__base_dir = '/sys/bus/w1/devices/'
        self.__device_path = glob.glob(self.__base_dir + '28*')[0] #get file path of sensor

    def __read_temp_raw(self):
        with open(self.__device_path +'/w1_slave','r') as f:
            valid, temp = f.readlines()
        return valid, temp
    
    def get_temp(self):
        valid, temp = self.__read_temp_raw()
        while 'YES' not in valid:
            time.sleep(0.2)
            valid, temp = self.__read_temp_raw()

        pos = temp.index('t=')
        if pos != -1:
            #read the temperature .
            temp_string = temp[pos+2:]
            self.temp = float(temp_string)/1000.0 
            return self.temp
        

# x = DS18B20()
# while True:
#     c = x.get_temp()
#     x.write_temp()
#     print('C={:,.3f}'.format(c))
#     time.sleep(1)
