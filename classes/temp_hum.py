import time
import board
import adafruit_am2320

class AM2315: 
    def __init__(self):
        self.__i2c = board.I2C()  # uses board.SCL and board.SDA
        self.__values = adafruit_am2320.AM2320(self.__i2c)
        self.temp = 0
        self.hum = 0
 
    def get_temp(self):
        self.temp = self.__values.temperature
        return self.temp
    
    def get_hum(self):
        self.hum = self.__values.relative_humidity
        return self.hum        

# x = AM2315()
# while True:
#     print("Temperature: ", x.get_temp())
#     print("Humidity: ", x.get_hum())
#     time.sleep(2)
