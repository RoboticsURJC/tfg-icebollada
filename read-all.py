#!/usr/bin/env python

import bme680
import time
import csv
import os
import matplotlib.pyplot as plt

if(os.path.exists("data.csv")):
   os.remove("data.csv")

start_time = time.time()

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


with open("data.csv", "a") as file:
    header = ['Seconds', 'Temperature', 'Pressure', 'Humidity', 'Gas resistance']
    writer = csv.DictWriter(file, fieldnames = header)
    writer.writeheader()          
                        
plt.ion()
fig = plt.figure(figsize=(16,16))
temp = fig.add_subplot(221)
press = fig.add_subplot(222)
hum = fig.add_subplot(223)
gas = fig.add_subplot(224)

def plot(x, y_temp, y_press, y_hum, y_gas):                    
    temp.set_title("Temperature measure")    
    temp.plot(x,y_temp,'-o', color='r')
    temp.set_xlabel("Seconds")
    temp.set_ylabel("Celsius")
        
    press.set_title("Pressure measure")
    press.plot(x,y_press,'-o', color='g')
    press.set_xlabel("Seconds")
    press.set_ylabel("Hecto Pascals")
        
    hum.set_title("Humidity measure")
    hum.plot(x,y_hum,'-o', color='b')
    hum.set_xlabel("Seconds")
    hum.set_ylabel("%Relatively Humidity")
        
    gas.set_title("Gas resistance measure")
    gas.plot(x,y_gas,'-o', color='purple')
    gas.set_xlabel("Seconds")
    gas.set_ylabel("Ohms")

    plt.show()
    plt.pause(1)   


x = []
y_temp = []
y_press = []
y_hum = []
y_gas = []

print('\n\nPolling:')
try:
    while True:
        if sensor.get_sensor_data():
            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)
            
            seconds = time.time() - start_time
            x.append(seconds)
            y_temp.append(sensor.data.temperature)
            y_press.append(sensor.data.pressure)
            y_hum.append(sensor.data.humidity)
            y_gas.append(sensor.data.gas_resistance)
            
            if sensor.data.heat_stable:
                print('{0},{1} Ohms'.format(
                    output,
                    sensor.data.gas_resistance))
                
                with open("data.csv", "a") as file:
                    writer = csv.DictWriter(file, fieldnames = header)
                    writer.writerow({'Seconds' : str(seconds),
                                        'Temperature': str(sensor.data.temperature), 
                                         'Pressure': str(sensor.data.pressure),
                                         'Humidity': str(sensor.data.humidity),
                                         'Gas resistance': str(sensor.data.gas_resistance)})
                    


            else:
                print(output)
                with open("data.csv", "a") as file:
                    writer = csv.DictWriter(file, fieldnames = header)
                    writer.writerow({'Seconds' : str(seconds),
                                        'Temperature': str(sensor.data.temperature), 
                                         'Pressure': str(sensor.data.pressure),
                                         'Humidity': str(sensor.data.humidity),
                                         'Gas resistance': 0})

            plot(x, y_temp, y_press, y_hum, y_gas)



except KeyboardInterrupt:
    pass
