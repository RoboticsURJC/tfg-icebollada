import ammonia
import bme
import temp_hum
import thermal_sensor
import waterdetector
import waterproof_temp
import time
import os
import csv
from threading import Thread


class all_sensors():
    def __init__(self):
        self.__header = ['Seconds', 'Temperature', 'Pressure', 'Humidity', 'Gas resistance', 'Waterproof temperature', 'Ammonia']
        self.__am = ammonia.MQ135()
        self.__bm = bme.BME680()
        #self.__th = temp_hum.AM2315()
        self.__thermal = thermal_sensor.AMG8833()
        self.__waterlev = waterdetector.waterLevel()
        self.__water_temp = waterproof_temp.DS18B20()
        self.__start_time = time.time()
        self.ammonia = 0
        self.bm_temp = 0
        self.bm_press = 0
        self.bm_hum = 0
        self.bm_gas_res = 0
        #self.th_temp = 0
        #self.th_hum = 0
        self.pixels = []
        self.level = 0
        self.wat_temp = 0

    def ammo(self):
        try:
            self.perc = self.__am.MQPercentage()
            self.ammonia = self.perc["NH3"]
        except:
            self.ammonia = self.__am.get_value()
            

    def bme(self):
        self.__bm.get_temp()
        self.bm_temp = self.__bm.get_temp()
        self.bm_press = self.__bm.get_press()
        self.bm_hum = self.__bm.get_hum()
        self.bm_gas_res = self.__bm.get_gas_res()
        
    def pix(self):
        self.pixels = self.__thermal.get_pixels()
        
    def lev(self):
        self.level = self.__waterlev.get_value()
        
    def water_t(self):
        self.wat_temp = self.__water_temp.get_temp()
        
    def write_values(self):
        seconds = time.time() - self.__start_time
        
        if(not os.path.exists("/home/pi/Desktop/classes/data.csv") or os.stat("/home/pi/Desktop/classes/data.csv").st_size == 0):
            with open("/home/pi/Desktop/classes/data.csv", "a") as file:
                writer = csv.DictWriter(file, fieldnames = self.__header)
                writer.writeheader()
        with open("/home/pi/Desktop/classes/data.csv", "a") as file:
                    writer = csv.DictWriter(file, fieldnames = self.__header)
                    writer.writerow({'Seconds' : str(seconds), 'Temperature' : str(self.bm_temp), 'Pressure' : str(self.bm_press),
                                     'Humidity' : str(self.bm_hum), 'Gas resistance' : str(self.bm_gas_res),
                                     'Waterproof temperature' : str(self.wat_temp), 'Ammonia' : str(self.ammonia)})
       

threads = []
x = all_sensors()

for func in [x.ammo, x.bme, x.pix, x.lev, x.water_t]:
    threads.append(Thread(target=func))
    threads[-1].start()
            
for thread in threads:
    thread.join()
    
x.write_values()

print("Ammonia:", round(x.ammonia,2), " Temperature:", x.bm_temp, " Pressure:", round(x.bm_press,1), " Humidity:", round(x.bm_hum, 1),
      " Gas:", round(x.bm_gas_res,1), " Water level:", x.level, " Waterproof temp:", x.wat_temp, " Pixels:", x.pixels)
     