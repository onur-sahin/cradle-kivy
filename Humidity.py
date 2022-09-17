from kivy.uix.boxlayout import BoxLayout
from kivy.properties import Clock

from DHT11_driver import DHT11_driver

from kivy.properties import NumericProperty

class HumidityBoxLayout(BoxLayout):

    humidity = NumericProperty()
    temp = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dht11 = DHT11_driver()

        Clock.schedule_interval(self.update, 2)


    def update(self, dt):
        self.temp, self.humidity = self.dht11.getTempAndHumidity()

