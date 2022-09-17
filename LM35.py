
if __name__!="__main__":
    from __main__ import adc
else:
    from ADC import ADC


from myTools import range_

    

class LM35:

    def __init__(self):
        self.adc = adc


    def getTempature(self):
        rawValue = self.adc.getSensorValue(channel=7)

        return range_(rawValue, 0, 65472, 0, 3.3*1000)/10




if __name__ == "__main__":

    adc = ADC()

    while True:

        temp = adc.getSensorValue(channel=7)

        print("LM35 tempature: " + str(temp) + " *C")