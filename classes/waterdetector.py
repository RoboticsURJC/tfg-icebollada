import adc
import time


class waterLevel:
    def __init__(self):
        self.__channel = 0
        self.__mcp = 0
        self.__mpc = adc.MCP3008(0)
        
    def get_value(self):
        return self.__mpc.analogInput(self.__channel)

# x = waterLevel()
# while True:
#     print(x.get_value())
#     time.sleep(0.5)


# while True:
#     print(mcp.analogInput(0))
#     
# if(mcp.analogInput(0) >= 0 and mcp.analogInput(0) < 80):
#     print(0)
# elif(mcp.analogInput(0) >= 80 and mcp.analogInput(0) < 120):
#     print(1)
# elif(mcp.analogInput(0) >= 120 and mcp.analogInput(0) < 140):
#     print(2)
# elif(mcp.analogInput(0) >= 140 and mcp.analogInput(0) < 300):
#     print(3)
#     print("CH0" +":", mcp.analogInput(0))
#     water_level = mcp.analogInput(0)/200.*100
#     print(str(water_level) +'%')
#     time.sleep(0.5)
    
    