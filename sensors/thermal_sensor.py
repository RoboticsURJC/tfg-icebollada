import busio
import board
import adafruit_amg88xx

class AMG8833:
    def __init__(self):
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.pixels = []
        
    def get_pixels(self):
        sensor = adafruit_amg88xx.AMG88XX(self.__i2c)
        self.pixels = sensor.pixels
        return self.pixels

# x = AMG8833()
# print(x.get_pixels())
