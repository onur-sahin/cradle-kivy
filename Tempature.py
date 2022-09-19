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
    
    warning = BooleanProperty(False)

    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

        self.lm35_driver = LM35()

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 0
        self.progbar.max = 44
        self.progbar.convert_to_percent_value = False
        
        self.progbar.label= Label(text="{}\u00B0C", font_size=40)
        
        self.btn = Button()
                         
        self.btn.bind(on_press=self.yeni)
                         
        
        self.add_widget(self.btn)
        self.add_widget(self.progbar)
        
    def yeni(self, self_button):
        print("#################")
      



    def update(self, dt):
        
        self.btn.size = self.size
        self.btn.pos = self.pos
        
        self.tempature = self.lm35_driver.getTempature()
        
        self.tempature = int(self.tempature)
        
        self.setColor()
        
        self.check_warning()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        

        self.progbar._value = self.tempature
        
        self.progbar._draw()
        
        
        
        
    def check_warning(self):
        
        
        if self.tempature < 20:
            self.warning = True
            
                    
        elif self.tempature > 26:
            self.warning = True
           
            
        else:
            self.warning = False
            

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
            self.progbar.progress_color = (1, 0.645, 0, 1)
            
        elif (t > 28 and t <= 32):  #TOO HOT  - RED
            self.progbar.progress_color = (1, 0, 0, 1)
        
        elif (t > 32):              #VERY HOT  - MAROON
            self.progbar.progress_color = (0.5, 0, 0, 1)





