

from myTools import range_


if __name__=="__main__":
    from ADC import ADC
    from time import sleep
    

    

class LM35:

    def __init__(self, adc):
        self.adc = adc


    def getTemperature(self):
        rawValue = self.adc.getSensorValue(channel=7)

        return range_(rawValue, 0, 65472, 0, 3.3*1000)/10




if __name__ == "__main__":

    adc = ADC()

    while True:

        temp = adc.getSensorValue(channel=7)
        
        temp = range_(temp, 0, 65472, 0, 3.3*1000)/10

        print("LM35 tempature: " + str(temp) + " *C")
        
        sleep(1)
