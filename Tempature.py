from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import Clock
from kivy.core.text import Label
from kivy.graphics import Line, Rectangle, Color

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar

from LM35 import LM35



class TempatureBoxLayout(FloatLayout):

    tempature = NumericProperty()
    
    cold_warning = BooleanProperty(False)
    hot_warning  = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        
        self.flag = True

        self.lm35_driver = LM35()
        
        self.tempature = 5
        

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 0
        self.progbar.max = 44
        self.progbar.convert_to_percent_value = False
        
        self.progbar.label= Label(text="{}\u00B0C", font_size=40)
        
        self.btn = Button(pos=self.pos,
                          size=self.size,
                          background_color=(0.2, 0.4, 0.5, 1)
                         )
        
        self.add_widget(self.btn)
        self.add_widget(self.progbar)



    def update(self, dt):
        
        
        
        
        self.btn.size = self.size
        self.btn.pos = self.pos
        
        self.tempature += 1 #self.lm35_driver.getTempature()
        
        self.tempature = int(self.tempature)
        
        self.setColor()
        
        self.warning()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        

        self.progbar._value = self.tempature
        
        self.progbar._draw()
        
        
        
        
    def warning(self):
        
        self.flag = not self.flag
        
        if self.tempature < 20:
            self.cold_warning = True
            
            self.btn.background_color = (0.2, 0.4, 0.5, 1 if self.flag==True else 0.5 )
            
        elif self.tempature > 26:
            self.hot_warning = True
            self.btn.background_color = (0.2, 0.4, 0.5, 1 if self.flag==True else 0.5 )
            
            
        else:
            self.btn.background_color = (0.2, 0.4, 0.5, 1)
            self.cold_warning = False
            self.hot_warning = False

    def setColor(self):
        
        t = self.tempature
        
        if (t < 18 ):               #TOO COLD - BLUE
            
            self.progbar.progress_color = (0, 0, 1, 1)
            
        elif (t >= 18 and t < 20):  #COLD     - TURQUAZ
            self.progbar.progress_color = (0, 1, 1, 1)
        
        elif (t >= 20 and t <= 24): #NORMAL   - GREEN
            self.progbar.progress_color = (0, 1, 0, 1)
        
        elif (t > 24 and t <= 26):  #WARM     - YELLOW
            self.progbar.progress_color = (1, 1, 0, 1)
            
        elif (t >26 and t <=28 ) :  #HOT      - ORANGE
            self.progbar.progress_color = (1, 0.647, 0, 1)
            
        elif (t > 28 ):             #TOO HOT  - RED
            self.progbar.progress_color = (1, 0, 0, 1)





