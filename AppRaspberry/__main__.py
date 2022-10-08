#!/usr/bin/env python
# -*- coding: utf-8 -*-



# One of the zillion rules of Kivy:
# Kivy looks for a .kv file with the same name as your App class in lowercase
# (minus “App” if it ends with ‘App’. eg. TutorialApp -> tutorial.kv)

# Compared to Python syntax, Kivy syntax really sucks.

# I would only use it if you have …




from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.app import App

from time import sleep
import threading

from ADC import ADC
from LM35 import LM35
from MQ135 import MQ135
from DHT11 import DHT11
from HallSensor import HallSensor
from FlameSensor import FlameSensor
from Mqtt_Driver import Mqtt_Driver
from FlameSensor import FlameSensor


from kivy.lang.builder import Builder

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.write()

#Builder.load_file("cradle.kv") This file is main .kv file, you don't need load again

Builder.load_file("lullaby.kv")
Builder.load_file("setting.kv")
Builder.load_file("cradle.kv")
Builder.load_file("air_quality.kv")
Builder.load_file("humidity.kv")
Builder.load_file("temperature.kv")







print("#####$$$$$")

class MainApp(App):

    def build(self):
        pass
        
    


class MessageButton(Button):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = ''
        


    def on_press(self):
        
        for idx, dct in enumerate(self.parent.parent.data):
            
            if dct["id"] == self.id:
                self.parent.parent.data.pop(idx)
                break
    



if __name__ == '__main__':
    
    adc = ADC()

    lm35_driver  = LM35(adc)
    mq135_driver = MQ135(adc)
    dht11_driver = DHT11()

    hallSensor = HallSensor()
    flameSensor = FlameSensor()


    mqtt_driver = Mqtt_Driver(lm35_driver,
                              mq135_driver,
                              dht11_driver,
                              flameSensor)
                              
    mqtt_thrd = threading.Thread(target=mqtt_driver.send_data )
    mqtt_thrd.start()
    
    MainApp().run()
    
