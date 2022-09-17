
import RPi.GPIO as gpio

from time import sleep

class HallSensor:

    hallpin = 21

    def __init__(self):
    
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup( HallSensor.hallpin, gpio.IN)


    def hallSensorState(self):
        return gpio.input(HallSensor.hallpin)





if __name__=="__main__":

    hallSensor = HallSensor()

    while True:

        if(hallSensor.hallSensorState() == False):

            print("magnet detected")

        else:

            print("magnetic field not detected")