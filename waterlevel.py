import spidev
import time

class MCP3008:
    def __init__(self, chip_select):
        self.spi = spidev.SpiDev()
        self.spi.open(0, chip_select)
        self.spi.max_speed_hz = 1000000

    def analogInput(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

mcp = MCP3008(0)

# while True:
#     print(mcp.analogInput(0))
#     
if(mcp.analogInput(0) >= 0 and mcp.analogInput(0) < 80):
    print(0)
elif(mcp.analogInput(0) >= 80 and mcp.analogInput(0) < 120):
    print(1)
elif(mcp.analogInput(0) >= 120 and mcp.analogInput(0) < 140):
    print(2)
elif(mcp.analogInput(0) >= 140 and mcp.analogInput(0) < 300):
    print(3)
#     print("CH0" +":", mcp.analogInput(0))
#     water_level = mcp.analogInput(0)/200.*100
#     print(str(water_level) +'%')
#     time.sleep(0.5)
    
    