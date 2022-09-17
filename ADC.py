
# sudo pip3 install adafruit-blinka
# sudo pip3 install adafruit-circuitpython-mcp3xxx

# before enable spi source:https://pimylifeup.com/raspberry-pi-spi/

# in terminal
# sudo raspi-config
# interfacing options -> Enable

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from time import sleep



class ADC ():
    
    #note:Since to use need to enable SPI in raspberry pi config

    # Create the SPI bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # Create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # Create the mcp object
    mcp = MCP.MCP3008(spi, cs)


    # Create analog inputs connected to the input pins on the MCP3008.

    channels = [0, 0, 0, 0, 0, 0, 0, 0]
   
    channels[0] = AnalogIn(mcp, MCP.P0)
    channels[1] = AnalogIn(mcp, MCP.P1)
    channels[2] = AnalogIn(mcp, MCP.P2)
    channels[3] = AnalogIn(mcp, MCP.P3)
    channels[4] = AnalogIn(mcp, MCP.P4)
    channels[5] = AnalogIn(mcp, MCP.P5)
    channels[6] = AnalogIn(mcp, MCP.P6)
    channels[7] = AnalogIn(mcp, MCP.P7)


    def getSensorValue(self, channel):

        # Read analog sensor values from the channel_X.
        
        # Returns the value of an ADC pin as an integer.
        # Due to 10-bit accuracy of the chip,
        # the returned values range [0, 65472].

        return  self.channels[channel].value 



if __name__ == "__main__":

    channel = 0
    sleep_time = 0.5

    adc = ADC()

    while(True):

        print("channel_", channel, ":" + str(adc.getSensorValue(channel)))

        sleep(sleep_time)  