
from time import sleep
import RPi.GPIO as gpio

class FlameSensor:
    
    flameSensorPin = 14
    
    def __init__(self):


        try:
    
            gpio.setmode(gpio.BCM)
            gpio.setwarnings(False)
            gpio.setup( self.flameSensorPin, gpio.IN)

        except:
            pass

    def flameSensorState(self):
        return gpio.input(self.flameSensorPin)






if __name__=="__main__":

    flameSensor = FlameSensor()

    while True:

        if(flameSensor.flameSensorState() == False):

            print("flame detected")

        else:

            print("flame not detected")
            
            
        sleep(0.01)
