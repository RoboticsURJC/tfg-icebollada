#!/usr/bin/env python

import bme680
import time

class BME680:
    def __init__(self):
        self.temp = 0
        self.press = 0
        self.hum = 0
        self.gas = 0
        
        try:
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.__sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

        for name in dir(self.__sensor.calibration_data):

            if not name.startswith('_'):
                value = getattr(self.__sensor.calibration_data, name)


        self.__sensor.set_humidity_oversample(bme680.OS_2X)
        self.__sensor.set_pressure_oversample(bme680.OS_4X)
        self.__sensor.set_temperature_oversample(bme680.OS_8X)
        self.__sensor.set_filter(bme680.FILTER_SIZE_3)
        self.__sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        for name in dir(self.__sensor.data):
            value = getattr(self.__sensor.data, name)

        self.__sensor.set_gas_heater_temperature(320)
        self.__sensor.set_gas_heater_duration(150)
        self.__sensor.select_gas_heater_profile(0)


    def get_temp(self):
        if self.__sensor.get_sensor_data():
            self.temp = self.__sensor.data.temperature
        else:
            self.temp = 0
        return self.temp
            
    def get_press(self):
        if self.__sensor.get_sensor_data():
            self.press = self.__sensor.data.pressure
        else:
            self.press = 0
        return self.press
            
    def get_hum(self):
        if self.__sensor.get_sensor_data():
            self.hum = self.__sensor.data.humidity
        else:
            self.hum = 0
        return self.hum
            
    def get_gas_res(self):
        if self.__sensor.get_sensor_data() and self.__sensor.data.heat_stable:
            self.gas = self.__sensor.data.gas_resistance 
        else:
            self.gas = 0
        return self.gas

# x = BME680()
# while True:
#     print(x.get_temp(), x.get_press(), x.get_hum(), x.get_gas_res())
#     time.sleep(3)
