from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.properties import Clock

from LM35 import LM35

class TempatureBoxLayout(BoxLayout):

    tempature = NumericProperty()
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 2)
        

        self.lm35_driver = LM35()


    def update(self, dt):
        self.tempature = self.lm35_driver.getTempature()


