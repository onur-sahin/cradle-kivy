from myTools import range_

if __name__=="__main__":
    from ADC import ADC
    from time import sleep



class MQ135:
    
    def __init__(self, adc):
        self.adc = adc
        
        
    def getAirQuality(self):
        

        self.rawValue = self.adc.getSensorValue( channel=0 )

        return self.calculatePPm( self.rawValue ) 


    def calculatePPm(self, rawValue):

        return range_(rawValue, 0, 65472, 10, 1000)



if __name__ == "__main__":
    
    adc = ADC()
    
    mq135_driver = MQ135(adc)
    
    while True:
        
        print( mq135_driver.getAirQuality() )
        
        sleep(1)
