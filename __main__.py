#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2022  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  




# One of the zillion rules of Kivy:
# Kivy looks for a .kv file with the same name as your App class in lowercase
# (minus “App” if it ends with ‘App’. eg. TutorialApp -> tutorial.kv)

# Compared to Python syntax, Kivy syntax really sucks.

# I would only use it if you have …

#from Cradle import HomeBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from ADC import ADC
from HallSensor import HallSensor

from kivy.lang.builder import Builder

from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')
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
