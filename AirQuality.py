#sudo pip3 install adafruit-blinka 
#for busio, digitalio, board

#sudo pip3 install adafruit-circuitpython-mcp3xxx


from kivy.uix.boxlayout import BoxLayout
from kivy.properties import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty

from time import sleep

from __main__ import adc
from myTools import range_



class AirQualityBoxLayout(BoxLayout):

    
    airQuality = StringProperty("waiting for calculation")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.adc = adc
        
        rawValue = -1

        Clock.schedule_interval(self.getAirQuality, 2)
        
    

    def getAirQuality(self, dt):

        self.rawValue = self.adc.getSensorValue( channel=0 )

        self.airQuality = str(  self.calculatePPm( self.rawValue )  )


    def calculatePPm(self, rawValue):

        return range_(rawValue, 0, 65472, 10, 1000)



#                    AQI Basics for Ozone and Particle Pollution

# Daily AQI Color   Levels of Concern Values of Index    Description of Air Quality
# Green	            Good                                 0 to 50	Air quality is satisfactory, and air pollution poses little or no risk.
# Yellow            Moderate                             51 to 100	Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.
# Orange            Unhealthy for Sensitive Groups	     101 to 150	Members of sensitive groups may experience health effects. The general public is less likely to be affected.
# Red               Unhealthy                            151 to 200	Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.
# Purple            Very Unhealthy                       201 to 300	Health alert: The risk of health effects is increased for everyone.
# Maroon            Hazardous                            301 and higher	Health warning of emergency conditions: everyone is more likely to be affected.