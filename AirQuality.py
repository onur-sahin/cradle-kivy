#sudo pip3 install adafruit-blinka 
#for busio, digitalio, board

#sudo pip3 install adafruit-circuitpython-mcp3xxx

if __name__!="__main__":
    from __main__ import adc

else:
    from ADC import ADC
    from time import sleep



from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.text import Label
from kivy.properties import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

from time import sleep
    
from myTools import range_

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar



class AirQualityBoxLayout(FloatLayout):

    
    # airQuality        = StringProperty("waiting for calculation")
    
    airQuality = NumericProperty()

    warning = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.adc = adc
        
        rawValue = -1

        Clock.schedule_interval(self.update, 1)
        

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 301
        self.progbar.max = 0
        self.progbar.convert_to_percent_value = True
        
        self.progbar.label = Label(text="{}\nPPM", font_size=40)
        
        self.btn = Button(pos=self.pos,
                          size=self.size
                          )

        self.btn.bind(on_press=self.yeni)

        self.add_widget(self.btn)
        self.add_widget(self.progbar)

    def yeni(self, self_button):
        print("####################")

    def update(self, dt):

        
        self.btn.size = self.size
        self.btn.pos = self.pos
        
        self.airQuality = self.getAirQuality()
        
        self.setColor()
        
        self.check_warning()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        

        self.progbar._value = self.airQuality
        
        self.progbar._draw()


    def check_warning(self):
        
        
        if self.airQuality >= 151:
            self.warning = True
    
        else:

            self.warning = False

    

    def setColor(self):
        
        p = self.airQuality
        
        if (p  >=0 and p <= 50 ):                           #GOOD         -GREEN
            
            self.progbar.progress_color = (0, 1, 0, 1)
            
        elif (p >= 51 and p <= 100):                        #MODERATE     -YELLOW
            self.progbar.progress_color = (1, 1, 0, 1)
         
        elif (p >= 101 and p <= 150):                       #UNHEALTY FOR SENSITIVE GROUPS- ORANGE
            self.progbar.progress_color = (1, 0.645, 0, 1)
        
        elif (p > 151 and p <= 200):                        #UNHEALTY     - RED
            self.progbar.progress_color = (1, 0, 0, 1)
            
        elif (p >= 201 and p <= 300 ) :                     #VERY UNHEALTY -PURPLE
            self.progbar.progress_color = (0.5, 0, 0.5, 1)
            
        elif (p >= 301):                                    #HAZARDOUS     -MAROON
            self.progbar.progress_color = (0.5, 0, 0, 1)

            


    
    def getAirQuality(self):

        self.rawValue = self.adc.getSensorValue( channel=0 )

        return self.calculatePPm( self.rawValue ) 


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



if __name__ == "__main__":
    
    adc = ADC()
    
    def calculatePPm(rawValue):

        return range_(rawValue, 0, 65472, 10, 1000)
    
    
    def getAirQuality(adc):

        rawValue = adc.getSensorValue( channel=0 )

        return calculatePPm( rawValue ) 
        
    count = 0
    
    while True:
        count += 1
        print(  f"{count}: AirQuality: {getAirQuality(adc)} PPM"  )
        
        sleep(1)
        
    
