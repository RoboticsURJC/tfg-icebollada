import busio
import board
import adafruit_amg88xx
import time

class AMG8833:
    def __init__(self):
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_amg88xx.AMG88XX(self.__i2c)
        
    def get_pixels(self):
        return self.sensor.pixels

x = AMG8833()
while(True):
    print(x.get_pixels())
    time.sleep(3)