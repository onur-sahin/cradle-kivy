
from time import sleep
import RPi.GPIO as gpio

class FlameSensor:
    
    flameSensorPin = 26
    
    def __init__(self):
    

        try:
    
            gpio.setmode(gpio.BCM)
            gpio.setwarnings(False)
            gpio.setup( self.flameSensorPin, gpio.IN)

        except BaseException as err:
            print("flame Sensor Error! :" + str(err) )
            

    def getFlameSensorState(self):
        
        while True:
            try:
                return gpio.input(self.flameSensorPin)
        
            except BaseException as err:
                print("getFlamSensorState() Error! :" + str(err))

            sleep(2)




if __name__=="__main__":

    flameSensor = FlameSensor()

    while True:

        if(flameSensor.flameSensorState() == False):

            print("flame detected")

        else:

            print("flame not detected")
            
            
        sleep(2)
