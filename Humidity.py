from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import Clock

from DHT11_driver import DHT11_driver

from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

from CircularProgressBar_Half.circular_progress_bar import CircularProgressBar



class HumidityBoxLayout(FloatLayout):

    humidity = NumericProperty()
    temp     = NumericProperty()

    warning  = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dht11 = DHT11_driver()

        Clock.schedule_interval(self.update, 1)

        self.progbar = CircularProgressBar()
        self.progbar.cap_style = "round"

        self.progbar.min = 0
        self.progbar.max = 100

        self.progbar.convert_to_percent_value = False
        
        self.progbar.label = Label(text="{}%", font_size=40)
        
        self.btn = Button(pos=self.pos,
                          size=self.size
                          )

        self.btn.bind(on_press=self.yeni)

        self.add_widget(self.btn)
        self.add_widget(self.progbar)

    def yeni(self, self_button):
        print("####################")


    def update(self, dt):
        self.temp, self.humidity = self.dht11.getTempAndHumidity()
















