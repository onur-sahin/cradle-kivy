from time import sleep
from statistics import mean
import RPi.GPIO as gpio
from datetime import datetime


if __name__!="__main__":
    from __main__ import adc
    
else:
    from ADC import ADC
    from myTools import range_


class SoundSensor:

    soundSensorPin = 20

    def __init__(self):
        gpio.setmode(gpio.BCM)
        
        gpio.setup(SoundSensor.soundSensorPin, gpio.IN)

        if(__name__!="__main__"):
            self.adc = adc

        self.raw_value = -1
        self.desibel = -1

    def soundSensorState(self):
    
        return gpio.input(SoundSensor.soundSensorPin)
    



if __name__=="__main__":

    digital = True

    sensor = SoundSensor()

    if digital:

        while digital:

            print("soundSensorDigital:", sensor.soundSensorState() )



    else:
        sleep_time = 1

        adc = ADC()

        raw_value = .0
        db_value = .0 

        raw_values = []
        db_values = []

        for i in range(0, 500):
            
            raw_values.append(.0)
            db_values.append(.0)

        

        while True:
            # raw_value = adc.getSensorValue(channel=3)
            # db_value = range_(raw_value, 0, 65472, 0, 120 )
            # print("raw_value/desibel:", raw_value,'/', db_value )


            for i in range(0, 500):
                
                raw_value = adc.getSensorValue(channel=3)
            
                db_value = range_(raw_value, 0, 65472, 0, 120 )
                raw_values[i] = raw_value
                db_values[i] = db_value
                
                
            print("raw_value/desibel:",max(raw_values),'/', max(db_values) )
            sleep(sleep_time)
            
            
            
            
            
