from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import Clock
from kivy.core.text import Label

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar

from LM35 import LM35



class TempatureBoxLayout(BoxLayout):

    tempature = NumericProperty()
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 2)

        self.lm35_driver = LM35()


        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"
        self.progbar.min = 0
        self.progbar.max = 360
        self.text_label= Label(text="{}\u00B0C", font_size=40)

        self.add_widget(self.progbar)



    def update(self, dt):
        self.tempature = self.lm35_driver.getTempature()

        self.progbar.widget_size = int(self.parent.size[1])
        self.progbar.pos = self.center_x-self.progbar.widget_size/2, self.center_y-self.progbar.widget_size/2
        self.progbar._value = self.tempature
        self.progbar._draw()





# class CircularProgressBar_FloatLayout(FloatLayout):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.progbar = CircularProgressBar()
#         self.progbar.cap_style = "round"
#         self.progbar.min = 0
#         self.progbar.max = 360
#         self.text_label= Label(text="{}\u00B0C", font_size=40)
    


#         self.add_widget(self.progbar)

#         Clock.schedule_interval(self.animate, 1)


#     def animate(self, dt):
#         self.progbar.widget_size = int(self.parent.size[1])
#         self.progbar.pos = self.parent.center_x-self.progbar.widget_size/2, self.parent.center_y-self.progbar.widget_size/2
#         self.progbar._value = self.root.tempature
#         self.progbar._draw()