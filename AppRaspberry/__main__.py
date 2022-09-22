#!/usr/bin/env python
# -*- coding: utf-8 -*-



# One of the zillion rules of Kivy:
# Kivy looks for a .kv file with the same name as your App class in lowercase
# (minus “App” if it ends with ‘App’. eg. TutorialApp -> tutorial.kv)

# Compared to Python syntax, Kivy syntax really sucks.

# I would only use it if you have …




from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from ADC import ADC
from HallSensor import HallSensor

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
Builder.load_file("tempature.kv")

adc = ADC()
hallSensor = HallSensor()


class MainApp(App):

    def build(self):
        pass




if __name__ == '__main__':

    MainApp().run()
