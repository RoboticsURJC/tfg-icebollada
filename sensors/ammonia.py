import adc
import time
import os

class MQ135:
    def __init__(self):
        self.__channel = 1
        self.__mcp = 0
        self.__mpc = adc.MCP3008(0)
        self.value = 0

    def get_value(self):
        self.value = self.__mpc.analogInput(self.__channel)
        return self.value
                   

# 
# x = MQ135()
# while True:
#     print(x.get_value())
#     
# #     print("CH0" +":", mcp.analogInput(0))
# #     water_level = mcp.analogInput(0)/200.*100
# #     print(str(water_level) +'%')
#     time.sleep(0.5)
    